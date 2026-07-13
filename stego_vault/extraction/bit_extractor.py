"""Extracción de datos ocultos en bits."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExtractionResult:
    """Resultado de extracción de datos."""
    method: str
    extracted_bytes: bytes
    extracted_text: str | None
    length: int
    description: str


class BitExtractor:
    """Extrae datos ocultos usando métodos de esteganografía."""

    def extract_lsb(self, data: bytes, num_bits: int = 8, bit_position: int = 0) -> bytes:
        bits = []
        for byte in data:
            bits.append((byte >> bit_position) & 1)

        result = bytearray()
        for i in range(0, len(bits) - num_bits + 1, num_bits):
            byte_val = 0
            for j in range(num_bits):
                byte_val = (byte_val << 1) | bits[i + j]
            result.append(byte_val)

        return bytes(result)

    def extract_lsb_text(self, data: bytes, bit_position: int = 0, max_length: int = 1000) -> ExtractionResult:
        extracted = self.extract_lsb(data, 8, bit_position)

        text = None
        try:
            decoded = extracted[:max_length].decode("utf-8", errors="replace")
            if any(c.isprintable() for c in decoded[:100]):
                text = decoded
        except Exception:
            pass

        return ExtractionResult(
            method="LSB Text",
            extracted_bytes=extracted[:max_length],
            extracted_text=text,
            length=len(extracted),
            description=f"Extraído {len(extracted)} bytes con método LSB (bit {bit_position})",
        )

    def extract_lsb_binary(self, data: bytes, bit_position: int = 0) -> ExtractionResult:
        extracted = self.extract_lsb(data, 8, bit_position)
        return ExtractionResult(
            method="LSB Binary",
            extracted_bytes=extracted,
            extracted_text=None,
            length=len(extracted),
            description=f"Extraído {len(extracted)} bytes binarios con método LSB",
        )

    def extract_at_offset(self, data: bytes, offset: int, length: int) -> ExtractionResult:
        extracted = data[offset:offset + length]
        return ExtractionResult(
            method="Offset extraction",
            extracted_bytes=extracted,
            extracted_text=None,
            length=len(extracted),
            description=f"Extraído {len(extracted)} bytes desde offset {offset}",
        )

    def detect_embedded_file(self, data: bytes) -> ExtractionResult | None:
        signatures = {
            b"\x89PNG": "PNG",
            b"\xff\xd8\xff": "JPEG",
            b"PK": "ZIP",
            b"%PDF": "PDF",
        }
        for sig, fmt in signatures.items():
            idx = data.find(sig, 1)
            if idx > 0:
                extracted = data[idx:]
                return ExtractionResult(
                    method="Embedded file",
                    extracted_bytes=extracted[:1024],
                    extracted_text=None,
                    length=len(extracted),
                    description=f"Archivo {fmt} embebido encontrado en offset {idx}",
                )
        return None
