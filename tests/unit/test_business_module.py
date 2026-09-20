import pytest
from businesses.core.base_module import BusinessMetadata, BusinessModule
from businesses.core.registry import BusinessRegistry
from businesses.solar_leads.module import SolarLeadsModule


@pytest.mark.asyncio
async def test_business_module_contract():
    meta = BusinessMetadata(
        business_id="test-biz-1",
        name="Test Business",
        description="A test business",
        status="DRAFT",
    )
    module = BusinessModule(meta)  # type: ignore

    # Default capability hooks should return not_implemented rather than raising
    res = await module.discover({})
    assert res["status"] == "not_implemented"
    assert res["capability"] == "discover"

    res_acquire = await module.acquire({})
    assert res_acquire["status"] == "not_implemented"


@pytest.mark.asyncio
async def test_solar_leads_draft_status():
    meta = BusinessMetadata(
        business_id="solar-biz-1",
        name="Solar Leads Express",
        description="Solar module in draft",
        status="DRAFT",
        acquisition_channels=["google_ads", "referrals"],
    )
    solar_module = SolarLeadsModule(meta)

    # In DRAFT, customer outreach should be blocked
    acquire_res = await solar_module.acquire({})
    assert acquire_res["status"] == "blocked"
    assert "DRAFT" in acquire_res["message"]

    # Qualification logic works without external calls
    qual_res = await solar_module.qualify({"monthly_electricity_bill": 2500.0})
    assert qual_res["qualified"] is True
    assert qual_res["score"] == 80.0

    unqual_res = await solar_module.qualify({"monthly_electricity_bill": 800.0})
    assert unqual_res["qualified"] is False


def test_business_registry():
    registered_cls = BusinessRegistry.get_module_class("solar_leads")
    assert registered_cls is SolarLeadsModule

    meta = BusinessMetadata(
        business_id="dyn-biz-1",
        name="Dynamic Solar",
        description="Instantiated from registry",
    )
    inst = BusinessRegistry.instantiate("solar_leads", meta)
    assert isinstance(inst, SolarLeadsModule)
