"""Tests para el detector de watermark."""

from stego_vault.detection.watermark_detector import WatermarkDetector


def test_detect_watermark():
    detector = WatermarkDetector()
    data = b"\xff\xd8\xff" + b"wm_test" + b"\x00" * 100
    results = detector.analyze(data)
    assert len(results) > 0


def test_no_watermark():
    detector = WatermarkDetector()
    import os
    data = os.urandom(200)
    results = detector.analyze(data)
    detected = [r for r in results if r.detected and r.watermark_type != "Repeated pattern"]
    assert len(detected) == 0


def test_repeated_patterns():
    detector = WatermarkDetector()
    pattern = b"\xaa\xbb\xcc\xdd" * 4
    data = pattern * 10
    result = detector.detect_repeated_patterns(data)
    assert result is not None
    assert result.detected is True


def test_get_detected():
    detector = WatermarkDetector()
    results = detector.analyze(b"wm_test" + b"\x00" * 100)
    detected = detector.get_detected(results)
    assert all(r.detected for r in detected)
