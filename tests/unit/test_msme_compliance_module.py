import io
import zipfile
import pytest
from businesses.core.registry import BusinessRegistry
from businesses.msme_compliance.config import MSMEComplianceConfig
from businesses.msme_compliance.module import MSMEComplianceModule
from businesses.msme_compliance.toolkit_generator import MSMEToolkitGenerator
from tools.finance.payment_provider import MockPaymentProvider, PaymentProviderFactory


def test_msme_compliance_config():
    config = MSMEComplianceConfig()
    assert config.module_name == "msme_compliance"
    assert config.status == "ACTIVE"
    assert len(config.pricing_tiers) >= 2
    starter = next(t for t in config.pricing_tiers if t.sku == "MSME-43BH-STARTER")
    pro = next(t for t in config.pricing_tiers if t.sku == "MSME-43BH-PRO-CA")
    assert starter.price_inr == 1999.0
    assert pro.price_inr == 3999.0


def test_msme_toolkit_generator():
    manifest = MSMEToolkitGenerator.get_template_manifest()
    assert len(manifest) >= 5
    filenames = [m["file_name"] for m in manifest]
    assert "01_CFO_Action_Guide_Section_43Bh.md" in filenames
    assert "02_Vendor_MSME_Status_Declaration_Form.txt" in filenames
    assert "03_Vendor_Written_Agreement_45Day_Addendum.txt" in filenames
    assert "04_Section_43Bh_Audit_Disallowance_Tracker.csv" in filenames
    assert "05_Section_16_MSMED_Compound_Interest_Calculator_SOP.md" in filenames

    # Check content generation
    guide_content = MSMEToolkitGenerator.get_document_content(
        "01_CFO_Action_Guide_Section_43Bh.md", company_name="Faridabad Castings Ltd"
    )
    assert "FARIDABAD CASTINGS LTD" in guide_content
    assert "Section 43B(h)" in guide_content

    # Check zip generation
    zip_bytes = MSMEToolkitGenerator.generate_zip_bundle(company_name="Faridabad Castings Ltd")
    assert len(zip_bytes) > 1000
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        infolist = zf.infolist()
        assert len(infolist) >= 5
        names = [info.filename for info in infolist]
        assert "04_Section_43Bh_Audit_Disallowance_Tracker.csv" in names


@pytest.mark.asyncio
async def test_msme_compliance_module_lifecycle():
    PaymentProviderFactory.reset()
    module = MSMEComplianceModule()
    assert module.status == "ACTIVE"
    assert module.name == "MSME Section 43B(h) Compliance Toolkit"

    # Discover
    disc = await module.discover({"target_region": "Delhi-NCR & Faridabad"})
    assert disc["status"] == "market_active"
    assert "Section 43B(h)" in disc["statutory_driver"]

    # Acquire
    acq = await module.acquire({"daily_budget": 500.0})
    assert acq["status"] == "active"
    assert acq["allowed_daily_budget_inr"] == 500.0

    # Qualify
    lead_sme = {
        "annual_turnover_inr": 25000000.0,
        "purchases_from_msme": True,
        "is_chartered_accountant": False,
    }
    qual_sme = await module.qualify(lead_sme)
    assert qual_sme["qualified"] is True
    assert qual_sme["recommended_sku"] == "MSME-43BH-STARTER"

    lead_ca = {
        "annual_turnover_inr": 0.0,
        "purchases_from_msme": False,
        "is_chartered_accountant": True,
    }
    qual_ca = await module.qualify(lead_ca)
    assert qual_ca["qualified"] is True
    assert qual_ca["recommended_sku"] == "MSME-43BH-PRO-CA"

    # Sell
    checkout = await module.sell({
        "sku": "MSME-43BH-STARTER",
        "email": "finance@delhicorporate.com",
        "name": "Rajesh Sharma",
    })
    assert checkout["status"] == "checkout_ready"
    assert checkout["amount_inr"] == 1999.0
    assert checkout["order_id"].startswith("order_mock_")

    # Fulfil
    fulfilment = await module.fulfil({
        "sku": "MSME-43BH-STARTER",
        "company_name": "Delhi Corporate Solutions",
    })
    assert fulfilment["status"] == "fulfilled"
    assert fulfilment["download_token"].startswith("dl_")
    assert len(fulfilment["delivered_files"]) >= 5

    # Collect with GST
    coll = await module.collect({"amount": 1999.0, "reference": "pay_mock_123"})
    assert coll["status"] == "recorded"
    assert coll["gross_amount_inr"] == 1999.0
    assert coll["gst_sac_code"] == "998311"
    assert coll["base_revenue_inr"] + coll["gst_collected_inr"] == 1999.0


def test_registry_registration():
    types = BusinessRegistry.list_available_types()
    assert "msme_compliance" in types
    cls = BusinessRegistry.get_module_class("msme_compliance")
    assert cls == MSMEComplianceModule
