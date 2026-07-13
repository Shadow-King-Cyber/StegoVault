"""Tests para el detector de metadatos."""

from stego_vault.detection.metadata_detector import MetadataDetector


def test_detect_signatures():
    detector = MetadataDetector()
    data = b"\xff\xd8\xff" + b"Exif\x00\x00" + b"test"
    found = detector.detect_signatures(data)
    assert "EXIF" in found


def test_analyze_metadata_suspicious():
    detector = MetadataDetector()
    metadata = {"Comment": "hidden data", "Make": "Canon"}
    result = detector.analyze_metadata(metadata)
    assert result.is_suspicious is True
    assert len(result.suspicious_fields) > 0


def test_analyze_metadata_clean():
    detector = MetadataDetector()
    metadata = {"Make": "Canon", "Model": "EOS"}
    result = detector.analyze_metadata(metadata)
    assert result.is_suspicious is False


def test_scan_raw_data():
    detector = MetadataDetector()
    data = b"\xff\xd8\xff" + b"Exif\x00\x00" + b"test"
    hidden = detector.scan_raw_data(data)
    assert len(hidden) > 0


def test_get_suspicious():
    detector = MetadataDetector()
    results = [
        detector.analyze_metadata({"Comment": "hidden"}),
        detector.analyze_metadata({"Make": "Canon"}),
    ]
    suspicious = detector.get_suspicious_findings(results)
    assert len(suspicious) == 1
