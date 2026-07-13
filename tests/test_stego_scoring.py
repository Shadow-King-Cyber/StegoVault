"""Tests para el scoring esteganográfico."""

from stego_vault.scoring.stego_scoring import StegoScoring


def test_score_clean():
    scoring = StegoScoring()
    result = scoring.calculate_score([])
    assert result.risk_level == "Limpio"
    assert result.score == 0


def test_score_with_lsb():
    scoring = StegoScoring()
    result = scoring.calculate_score(["LSB detection found"])
    assert result.high_risk == 1
    assert result.score >= 3


def test_score_with_metadata():
    scoring = StegoScoring()
    result = scoring.calculate_score(["Metadata suspicious"])
    assert result.medium_risk == 1


def test_owasp_mapping():
    scoring = StegoScoring()
    mapping = scoring.get_owasp_mapping()
    assert "Data Hiding" in mapping
    assert len(mapping) == 3
