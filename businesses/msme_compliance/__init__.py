from businesses.core.registry import BusinessRegistry
from businesses.msme_compliance.config import MSMEComplianceConfig
from businesses.msme_compliance.module import MSMEComplianceModule
from businesses.msme_compliance.toolkit_generator import MSMEToolkitGenerator

BusinessRegistry.register("msme_compliance", MSMEComplianceModule)

__all__ = ["MSMEComplianceConfig", "MSMEComplianceModule", "MSMEToolkitGenerator"]
