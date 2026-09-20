import pytest
from agents.core.evidence import Finding, FindingClassification


def test_finding_creation_and_attributes():
    finding = Finding.create_and_verify(
        source_url="https://cpcb.nic.in/waste-rules",
        source_title="CPCB Used Oil Framework",
        source_domain="cpcb.nic.in",
        classification=FindingClassification.FACT,
        content_summary="Authorized aggregators must register manifests.",
        confidence=0.95,
        publication_date="2023-11-01",
    )

    assert finding.classification == FindingClassification.FACT
    assert finding.source_domain == "cpcb.nic.in"
    assert finding.confidence == 0.95
    assert finding.finding_id is not None
    assert finding.retrieved_at is not None


def test_integrity_rule_prevent_silent_conversion_of_estimate_to_fact():
    """
    Section 3 Requirement:
    The Research Agent must never silently convert an estimate into a fact.
    """
    # Attempting to classify text containing "estimate" or "projected" as a FACT should raise ValueError
    with pytest.raises(ValueError, match="Cannot classify evidence containing estimate keyword"):
        Finding.create_and_verify(
            source_url="https://market-reports.internal/cac",
            source_title="Market Survey",
            source_domain="market-reports.internal",
            classification=FindingClassification.FACT,  # Illegal conversion
            content_summary="Installers report an estimated 1,200 INR customer acquisition cost.",
        )

    with pytest.raises(ValueError, match="Cannot classify evidence containing estimate keyword"):
        Finding.create_and_verify(
            source_url="https://market-reports.internal/cac",
            source_title="Market Survey",
            source_domain="market-reports.internal",
            classification=FindingClassification.FACT,
            content_summary="Revenue is projected to reach 50,000 INR monthly.",
        )


def test_valid_estimate_and_claim_classification():
    finding_est = Finding.create_and_verify(
        source_url="https://market-reports.internal/cac",
        source_title="Market Survey",
        source_domain="market-reports.internal",
        classification=FindingClassification.ESTIMATE,
        content_summary="Installers report an estimated 1,200 INR customer acquisition cost.",
    )
    assert finding_est.classification == FindingClassification.ESTIMATE

    finding_claim = Finding.create_and_verify(
        source_url="https://pv-magazine.internal/forum",
        source_title="Industry Forum",
        source_domain="pv-magazine.internal",
        classification=FindingClassification.CLAIM,
        content_summary="Vendors claimed 60% of digital leads fail phone verification.",
    )
    assert finding_claim.classification == FindingClassification.CLAIM
