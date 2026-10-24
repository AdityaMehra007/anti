"""
Global Maritime Supply Chain & Chokepoint Logistics Optimizer
Simulates strategic ocean trade corridors, transit time, bunker fuel economics,
chokepoint disruption rerouting (Suez vs Cape of Good Hope), and Demurrage & Detention (D&D) penalties.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class Chokepoint(Enum):
    SUEZ_CANAL = "Suez Canal / Red Sea"
    PANAMA_CANAL = "Panama Canal"
    STRAIT_OF_MALACCA = "Strait of Malacca"
    CAPE_OF_GOOD_HOPE = "Cape of Good Hope"
    STRAIT_OF_HORMUZ = "Strait of Hormuz"


@dataclass
class MaritimeRouteSpec:
    route_id: str
    origin_port: str
    destination_port: str
    primary_chokepoints: List[Chokepoint]
    distance_nautical_miles: float
    standard_speed_knots: float = 18.0
    canal_tolls_usd: float = 350_000.0
    bunker_fuel_price_usd_per_ton: float = 620.0
    daily_fuel_consumption_tons: float = 45.0

    @property
    def transit_days(self) -> float:
        hours = self.distance_nautical_miles / self.standard_speed_knots
        return round(hours / 24.0, 1)

    @property
    def total_bunker_fuel_cost_usd(self) -> float:
        total_tons = self.transit_days * self.daily_fuel_consumption_tons
        return round(total_tons * self.bunker_fuel_price_usd_per_ton, 2)

    @property
    def total_voyage_cost_usd(self) -> float:
        return round(self.total_bunker_fuel_cost_usd + self.canal_tolls_usd, 2)


class MaritimeSupplyChainOptimizer:
    """Institutional routing and disruption analysis engine for global container carriers."""

    @staticmethod
    def get_corridor_catalog() -> Dict[str, MaritimeRouteSpec]:
        return {
            "ASIA_EUROPE_SUEZ": MaritimeRouteSpec(
                route_id="ASIA_EUROPE_SUEZ",
                origin_port="Shanghai Port",
                destination_port="Rotterdam Port",
                primary_chokepoints=[Chokepoint.STRAIT_OF_MALACCA, Chokepoint.SUEZ_CANAL],
                distance_nautical_miles=10_500.0,
                canal_tolls_usd=400_000.0
            ),
            "ASIA_EUROPE_CAPE": MaritimeRouteSpec(
                route_id="ASIA_EUROPE_CAPE",
                origin_port="Shanghai Port",
                destination_port="Rotterdam Port",
                primary_chokepoints=[Chokepoint.CAPE_OF_GOOD_HOPE],
                distance_nautical_miles=14_000.0,
                canal_tolls_usd=0.0  # Avoids Suez toll
            ),
            "TRANS_PACIFIC": MaritimeRouteSpec(
                route_id="TRANS_PACIFIC",
                origin_port="Shenzhen Port",
                destination_port="Port of Los Angeles",
                primary_chokepoints=[],
                distance_nautical_miles=6_500.0,
                canal_tolls_usd=0.0
            ),
            "MIDDLE_EAST_INDIA": MaritimeRouteSpec(
                route_id="MIDDLE_EAST_INDIA",
                origin_port="Jebel Ali (Dubai)",
                destination_port="Nhava Sheva (JNPT)",
                primary_chokepoints=[Chokepoint.STRAIT_OF_HORMUZ],
                distance_nautical_miles=1_200.0,
                canal_tolls_usd=0.0
            )
        }

    @staticmethod
    def simulate_chokepoint_blockade(
        disrupted_chokepoint: Chokepoint = Chokepoint.SUEZ_CANAL
    ) -> Dict[str, Any]:
        """
        Simulates disruption impacts when a major maritime artery is closed.
        Example: Suez closure forces rerouting around Cape of Good Hope.
        """
        catalog = MaritimeSupplyChainOptimizer.get_corridor_catalog()
        base_route = catalog["ASIA_EUROPE_SUEZ"]
        rerouted = catalog["ASIA_EUROPE_CAPE"]

        delta_distance = rerouted.distance_nautical_miles - base_route.distance_nautical_miles
        delta_days = rerouted.transit_days - base_route.transit_days
        delta_bunker = rerouted.total_bunker_fuel_cost_usd - base_route.total_bunker_fuel_cost_usd
        net_voyage_cost_diff = rerouted.total_voyage_cost_usd - base_route.total_voyage_cost_usd

        return {
            "disrupted_chokepoint": disrupted_chokepoint.value,
            "status": "DISRUPTED_REROUTING_REQUIRED",
            "primary_route": base_route.route_id,
            "alternate_route": rerouted.route_id,
            "base_transit_days": base_route.transit_days,
            "rerouted_transit_days": rerouted.transit_days,
            "additional_transit_days": round(delta_days, 1),
            "additional_nautical_miles": round(delta_distance, 1),
            "bunker_cost_increase_usd": round(delta_bunker, 2),
            "canal_toll_saved_usd": base_route.canal_tolls_usd,
            "net_voyage_cost_difference_usd": round(net_voyage_cost_diff, 2),
            "freight_rate_spike_indicator_pct": 35.0  # Expected market spot freight increase
        }

    @staticmethod
    def compute_demurrage_and_detention(
        teu_containers: int,
        port_delay_days: int,
        free_days_allowed: int = 5,
        daily_rate_tier1_usd: float = 150.0,
        daily_rate_tier2_usd: float = 300.0
    ) -> Dict[str, Any]:
        """
        Calculates port demurrage & detention liability for delayed container clearances.
        Tier 1 applies for days 1-5 beyond free time; Tier 2 applies thereafter.
        """
        chargeable_days = max(0, port_delay_days - free_days_allowed)
        if chargeable_days == 0:
            return {
                "teu_containers": teu_containers,
                "port_delay_days": port_delay_days,
                "free_days_allowed": free_days_allowed,
                "chargeable_days": 0,
                "total_demurrage_usd": 0.0,
                "risk_rating": "LOW_CLEARED_ON_TIME"
            }

        tier1_days = min(5, chargeable_days)
        tier2_days = max(0, chargeable_days - 5)

        charge_per_container = (tier1_days * daily_rate_tier1_usd) + (tier2_days * daily_rate_tier2_usd)
        total_demurrage = round(teu_containers * charge_per_container, 2)

        risk = "HIGH_COST_IMPACT" if total_demurrage > 100_000.0 else "MODERATE_DELAY"

        return {
            "teu_containers": teu_containers,
            "port_delay_days": port_delay_days,
            "free_days_allowed": free_days_allowed,
            "chargeable_days": chargeable_days,
            "tier1_days": tier1_days,
            "tier2_days": tier2_days,
            "charge_per_teu_usd": round(charge_per_container, 2),
            "total_demurrage_usd": total_demurrage,
            "risk_rating": risk
        }
