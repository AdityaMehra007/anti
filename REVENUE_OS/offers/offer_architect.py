"""Offers forwarder module."""
import importlib

_mod = importlib.import_module("REVENUE_OS.07_OFFERS.offer_architect")
OfferArchitect = _mod.OfferArchitect

__all__ = ["OfferArchitect"]
