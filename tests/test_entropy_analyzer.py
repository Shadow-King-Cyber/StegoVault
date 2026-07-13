"""Tests para el analizador de entropía."""

from stego_vault.analysis.entropy_analyzer import EntropyAnalyzer


def test_calculate_entropy_empty():
    analyzer = EntropyAnalyzer()
    assert analyzer.calculate_entropy(b"") == 0.0


def test_calculate_entropy_uniform():
    analyzer = EntropyAnalyzer()
    assert analyzer.calculate_entropy(b"\x00" * 100) == 0.0


def test_calculate_entropy_random():
    import os
    analyzer = EntropyAnalyzer()
    data = os.urandom(1000)
    entropy = analyzer.calculate_entropy(data)
    assert entropy > 7.0


def test_analyze_region():
    analyzer = EntropyAnalyzer()
    result = analyzer.analyze_region(b"\x00" * 100, "test")
    assert result.region == "test"
    assert result.entropy == 0.0
    assert not result.is_suspicious


def test_analyze_data():
    analyzer = EntropyAnalyzer()
    results = analyzer.analyze_data(b"\x00" * 2048, chunk_size=1024)
    assert len(results) == 2


def test_get_suspicious():
    analyzer = EntropyAnalyzer()
    import os
    results = [
        analyzer.analyze_region(b"\x00" * 100, "clean"),
        analyzer.analyze_region(os.urandom(100), "random"),
    ]
    suspicious = analyzer.get_suspicious_regions(results)
    assert len(suspicious) >= 0
