from businesses.core.registry import BusinessRegistry
from businesses.solar_leads.module import SolarLeadsModule
from businesses.solar_leads.config import SolarLeadConfig

BusinessRegistry.register("solar_leads", SolarLeadsModule)

__all__ = ["SolarLeadsModule", "SolarLeadConfig"]
