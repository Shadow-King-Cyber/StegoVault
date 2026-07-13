"""Tests para el detector LSB."""

from stego_vault.detection.lsb_detector import LSBDetector


def test_extract_lsb():
    detector = LSBDetector()
    bits = detector.extract_lsb(b"\xff\x00", bit_position=0)
    assert bits == [1, 0]


def test_analyze_channel():
    detector = LSBDetector()
    result = detector.analyze_channel(b"\x00" * 100, "R")
    assert result.channel == "R"
    assert result.bits_analyzed == 100


def test_analyze_rgb():
    detector = LSBDetector()
    data = bytes([255, 128, 64] * 100)
    results = detector.analyze_rgb(data)
    assert len(results) == 3


def test_get_suspicious():
    detector = LSBDetector()
    results = [
        detector.analyze_channel(b"\xff" * 100, "R"),
        detector.analyze_channel(b"\x00" * 100, "G"),
    ]
    suspicious = detector.get_suspicious_channels(results)
    assert isinstance(suspicious, list)
