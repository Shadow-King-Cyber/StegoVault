"""Tests para el constructor de reportes."""

from stego_vault.reporting.report_builder import ReportBuilder, ReportData


def test_build_summary_empty():
    builder = ReportBuilder()
    result = builder.build_summary([])
    assert result["total"] == 0


def test_build_summary_with_entries():
    builder = ReportBuilder()
    entries = [
        {"analysis_type": "entropy", "findings": 2},
        {"analysis_type": "lsb", "findings": 1},
    ]
    result = builder.build_summary(entries)
    assert result["total"] == 2
    assert "entropy" in result["analysis_types"]


def test_build_report():
    builder = ReportBuilder()
    data = ReportData(
        filename="test.png",
        file_format="PNG",
        total_findings=3,
        risk_level="Alto",
        risk_score=6,
        owasp_mapping={"Data Hiding": "A08:2021"},
        entries=[],
    )
    report = builder.build_report(data)
    assert report["tool"] == "StegoVault"
    assert report["filename"] == "test.png"
    assert report["summary"]["risk_level"] == "Alto"
