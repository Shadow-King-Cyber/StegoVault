"""Tests para el analizador de consistencia."""

from stego_vault.analysis.consistency_analyzer import ConsistencyAnalyzer


def test_check_file_signature_png():
    analyzer = ConsistencyAnalyzer()
    result = analyzer.check_file_signature(b"\x89PNG\r\n\x1a\n", "png")
    assert result.is_consistent is True


def test_check_file_signature_mismatch():
    analyzer = ConsistencyAnalyzer()
    result = analyzer.check_file_signature(b"\xff\xd8\xff", "png")
    assert result.is_consistent is False


def test_check_file_size_ok():
    analyzer = ConsistencyAnalyzer()
    result = analyzer.check_file_size(b"\x00" * 1000)
    assert result.is_consistent is True


def test_check_file_size_too_small():
    analyzer = ConsistencyAnalyzer()
    result = analyzer.check_file_size(b"\x00" * 5)
    assert result.is_consistent is False


def test_check_trailing_data():
    analyzer = ConsistencyAnalyzer()
    result = analyzer.check_trailing_data(b"\x89PNG" + b"\x00" * 2000)
    assert result.is_consistent is False
    assert "nulos" in result.description


def test_run_all_checks():
    analyzer = ConsistencyAnalyzer()
    results = analyzer.run_all_checks(b"\x89PNG" + b"\x00" * 500, "png")
    assert len(results) == 3
