"""
Stock Market & Equities Quantitative Execution Engine
Provides limit order book mechanics, multi-factor alpha scoring, algorithmic execution (TWAP/VWAP),
and portfolio risk optimization (Sharpe, Parametric VaR, Expected Shortfall).
"""
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Tuple, Optional


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


@dataclass
class Order:
    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    price: float
    quantity: int
    filled_quantity: int = 0
    timestamp: float = 0.0

    @property
    def remaining_quantity(self) -> int:
        return self.quantity - self.filled_quantity


@dataclass
class TradeExecution:
    trade_id: str
    symbol: str
    price: float
    quantity: int
    buyer_order_id: str
    seller_order_id: str
    timestamp: float


class LimitOrderBook:
    """Institutional-grade L2 Limit Order Book with Price-Time priority matching."""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids: List[Order] = []  # Sorted descending by price, then ascending timestamp
        self.asks: List[Order] = []  # Sorted ascending by price, then ascending timestamp
        self.trade_history: List[TradeExecution] = []
        self._trade_counter = 0

    def add_order(self, order: Order) -> List[TradeExecution]:
        fills: List[TradeExecution] = []
        if order.order_type == OrderType.MARKET:
            fills = self._match_market_order(order)
        else:
            fills = self._match_limit_order(order)
        return fills

    def _match_market_order(self, order: Order) -> List[TradeExecution]:
        fills = []
        book_side = self.asks if order.side == OrderSide.BUY else self.bids
        while book_side and order.remaining_quantity > 0:
            best_maker = book_side[0]
            matched_qty = min(order.remaining_quantity, best_maker.remaining_quantity)
            execution_price = best_maker.price

            self._trade_counter += 1
            fill = TradeExecution(
                trade_id=f"TRD-{self._trade_counter:06d}",
                symbol=self.symbol,
                price=execution_price,
                quantity=matched_qty,
                buyer_order_id=order.order_id if order.side == OrderSide.BUY else best_maker.order_id,
                seller_order_id=best_maker.order_id if order.side == OrderSide.BUY else order.order_id,
                timestamp=order.timestamp
            )
            fills.append(fill)
            self.trade_history.append(fill)

            order.filled_quantity += matched_qty
            best_maker.filled_quantity += matched_qty

            if best_maker.remaining_quantity == 0:
                book_side.pop(0)

        return fills

    def _match_limit_order(self, order: Order) -> List[TradeExecution]:
        fills = []
        opposite_side = self.asks if order.side == OrderSide.BUY else self.bids

        while opposite_side and order.remaining_quantity > 0:
            best_maker = opposite_side[0]
            # Check price cross
            if (order.side == OrderSide.BUY and order.price >= best_maker.price) or \
               (order.side == OrderSide.SELL and order.price <= best_maker.price):
                matched_qty = min(order.remaining_quantity, best_maker.remaining_quantity)
                execution_price = best_maker.price

                self._trade_counter += 1
                fill = TradeExecution(
                    trade_id=f"TRD-{self._trade_counter:06d}",
                    symbol=self.symbol,
                    price=execution_price,
                    quantity=matched_qty,
                    buyer_order_id=order.order_id if order.side == OrderSide.BUY else best_maker.order_id,
                    seller_order_id=best_maker.order_id if order.side == OrderSide.BUY else order.order_id,
                    timestamp=order.timestamp
                )
                fills.append(fill)
                self.trade_history.append(fill)

                order.filled_quantity += matched_qty
                best_maker.filled_quantity += matched_qty

                if best_maker.remaining_quantity == 0:
                    opposite_side.pop(0)
            else:
                break

        # Resting remainder added to book
        if order.remaining_quantity > 0:
            if order.side == OrderSide.BUY:
                self.bids.append(order)
                self.bids.sort(key=lambda o: (-o.price, o.timestamp))
            else:
                self.asks.append(order)
                self.asks.sort(key=lambda o: (o.price, o.timestamp))

        return fills

    def get_order_book_depth(self) -> Dict[str, any]:
        best_bid = self.bids[0].price if self.bids else None
        best_ask = self.asks[0].price if self.asks else None
        spread = round(best_ask - best_bid, 4) if (best_bid and best_ask) else None
        mid = round((best_ask + best_bid) / 2.0, 4) if (best_bid and best_ask) else None

        bid_depth = sum(o.remaining_quantity for o in self.bids)
        ask_depth = sum(o.remaining_quantity for o in self.asks)

        return {
            "symbol": self.symbol,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": spread,
            "mid_price": mid,
            "bid_volume": bid_depth,
            "ask_volume": ask_depth,
            "top_bids": [(o.price, o.remaining_quantity) for o in self.bids[:5]],
            "top_asks": [(o.price, o.remaining_quantity) for o in self.asks[:5]]
        }


@dataclass
class EquityFactorProfile:
    symbol: str
    company_name: str
    sector: str
    current_price: float
    momentum_12m_pct: float
    earnings_yield_pct: float
    roic_pct: float
    debt_to_equity: float
    realized_volatility_pct: float

    def compute_composite_alpha(self) -> float:
        """
        Calculates multi-factor institutional alpha:
        35% Momentum + 25% Quality (ROIC) + 20% Value (Earnings Yield) + 20% Low-Vol/Solvency.
        """
        norm_mom = min(max(self.momentum_12m_pct / 50.0, -1.0), 2.0)
        norm_qual = min(max(self.roic_pct / 40.0, -0.5), 2.0)
        norm_val = min(max(self.earnings_yield_pct / 10.0, -0.5), 2.0)
        leverage_penalty = max(0.0, (self.debt_to_equity - 1.0) * 0.2)
        vol_score = max(0.0, (30.0 - self.realized_volatility_pct) / 20.0)

        alpha = (norm_mom * 0.35) + (norm_qual * 0.25) + (norm_val * 0.20) + (vol_score * 0.20) - leverage_penalty
        return round(alpha * 10.0, 2)


class AlgorithmicExecutionSlicer:
    """Generates TWAP and VWAP institutional order execution schedules."""

    @staticmethod
    def generate_twap_schedule(total_quantity: int, duration_minutes: int, interval_minutes: int = 5) -> List[Dict[str, any]]:
        intervals = max(1, duration_minutes // interval_minutes)
        base_slice = total_quantity // intervals
        remainder = total_quantity % intervals

        schedule = []
        for i in range(intervals):
            qty = base_slice + (1 if i < remainder else 0)
            schedule.append({
                "interval_index": i + 1,
                "minute_mark": (i + 1) * interval_minutes,
                "target_quantity": qty
            })
        return schedule

    @staticmethod
    def generate_vwap_schedule(total_quantity: int, historical_hourly_distribution: List[float]) -> List[Dict[str, any]]:
        """Distributes order slices following intraday U-shaped volume curve profile."""
        total_dist = sum(historical_hourly_distribution)
        if total_dist == 0:
            weights = [1.0 / len(historical_hourly_distribution)] * len(historical_hourly_distribution)
        else:
            weights = [w / total_dist for w in historical_hourly_distribution]

        schedule = []
        allocated_so_far = 0
        for i, weight in enumerate(weights):
            if i == len(weights) - 1:
                qty = total_quantity - allocated_so_far
            else:
                qty = int(round(total_quantity * weight))
                allocated_so_far += qty
            schedule.append({
                "bucket_index": i + 1,
                "volume_weight_pct": round(weight * 100.0, 2),
                "allocated_quantity": max(0, qty)
            })
        return schedule


class PortfolioRiskOptimizer:
    """Computes portfolio variance, Sharpe ratio, Parametric VaR, and Conditional VaR (Expected Shortfall)."""

    @staticmethod
    def evaluate_portfolio(
        weights: List[float],
        expected_returns: List[float],
        volatilities: List[float],
        correlation_matrix: List[List[float]],
        risk_free_rate: float = 0.045,
        portfolio_value_usd: float = 10_000_000.0
    ) -> Dict[str, float]:
        n = len(weights)
        if sum(weights) == 0:
            weights = [1.0 / n] * n
        else:
            w_sum = sum(weights)
            weights = [w / w_sum for w in weights]

        # Expected return
        port_return = sum(weights[i] * expected_returns[i] for i in range(n))

        # Portfolio variance = w^T * Cov * w
        port_variance = 0.0
        for i in range(n):
            for j in range(n):
                cov_ij = correlation_matrix[i][j] * volatilities[i] * volatilities[j]
                port_variance += weights[i] * weights[j] * cov_ij

        port_volatility = math.sqrt(max(port_variance, 1e-9))
        sharpe_ratio = (port_return - risk_free_rate) / port_volatility if port_volatility > 0 else 0.0

        # Parametric Value at Risk (1-day, assuming 252 trading days/year)
        daily_vol = port_volatility / math.sqrt(252.0)
        daily_ret = port_return / 252.0

        # Z-scores: 95% = 1.6449, 99% = 2.3263
        var_95_pct = (1.6449 * daily_vol) - daily_ret
        var_99_pct = (2.3263 * daily_vol) - daily_ret
        var_95_usd = round(var_95_pct * portfolio_value_usd, 2)
        var_99_usd = round(var_99_pct * portfolio_value_usd, 2)

        # Expected Shortfall (CVaR 95% under normal distribution)
        # ES = daily_vol * (phi(z) / (1 - alpha)) - daily_ret where phi(1.645) ~ 0.1031
        cvar_95_pct = daily_vol * (0.103135 / 0.05) - daily_ret
        cvar_95_usd = round(cvar_95_pct * portfolio_value_usd, 2)

        return {
            "portfolio_value_usd": portfolio_value_usd,
            "expected_annual_return_pct": round(port_return * 100.0, 2),
            "annualized_volatility_pct": round(port_volatility * 100.0, 2),
            "sharpe_ratio": round(sharpe_ratio, 3),
            "daily_var_95_pct": round(var_95_pct * 100.0, 3),
            "daily_var_95_usd": var_95_usd,
            "daily_var_99_usd": var_99_usd,
            "daily_cvar_95_usd": cvar_95_usd
        }
