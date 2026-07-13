"""Tests para el extractor de bits."""

from stego_vault.extraction.bit_extractor import BitExtractor


def test_extract_lsb():
    extractor = BitExtractor()
    data = bytes([0b10101010] * 8)
    result = extractor.extract_lsb(data, 8, 0)
    assert len(result) > 0


def test_extract_lsb_text():
    extractor = BitExtractor()
    data = b"\x00" * 100
    result = extractor.extract_lsb_text(data)
    assert result.method == "LSB Text"
    assert result.length > 0


def test_extract_lsb_binary():
    extractor = BitExtractor()
    data = b"\xff" * 100
    result = extractor.extract_lsb_binary(data)
    assert result.method == "LSB Binary"


def test_extract_at_offset():
    extractor = BitExtractor()
    data = b"AAAA" + b"SECRET" + b"BBBB"
    result = extractor.extract_at_offset(data, 4, 6)
    assert result.extracted_bytes == b"SECRET"


def test_detect_embedded_file():
    extractor = BitExtractor()
    data = b"\x00\x00\x00" + b"\x89PNG" + b"\x00" * 100
    result = extractor.detect_embedded_file(data)
    assert result is not None
    assert "PNG" in result.description
