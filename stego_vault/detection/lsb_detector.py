"""Detector de esteganografía LSB (Least Significant Bit)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LSBDetectionResult:
    """Resultado de detección LSB."""
    channel: str
    bits_analyzed: int
    suspicious_count: int
    ratio: float
    is_suspicious: bool
    description: str


class LSBDetector:
    """Detecta datos ocultos usando análisis de bits menos significativos."""

    SUSPICIOUS_RATIO = 0.6

    def extract_lsb(self, data: bytes, bit_position: int = 0) -> list[int]:
        bits = []
        for byte in data:
            bits.append((byte >> bit_position) & 1)
        return bits

    def analyze_channel(self, data: bytes, channel_name: str, bit_position: int = 0) -> LSBDetectionResult:
        bits = self.extract_lsb(data, bit_position)
        total = len(bits)
        if total == 0:
            return LSBDetectionResult(
                channel=channel_name,
                bits_analyzed=0,
                suspicious_count=0,
                ratio=0.0,
                is_suspicious=False,
                description="Sin datos para analizar",
            )

        ones = sum(bits)
        ratio = ones / total
        is_suspicious = ratio > self.SUSPICIOUS_RATIO or ratio < (1 - self.SUSPICIOUS_RATIO)

        if is_suspicious:
            desc = f"Distribución anómala de LSB en {channel_name} (ratio: {ratio:.2f})"
        else:
            desc = f"Distribución normal de LSB en {channel_name} (ratio: {ratio:.2f})"

        return LSBDetectionResult(
            channel=channel_name,
            bits_analyzed=total,
            suspicious_count=ones,
            ratio=ratio,
            is_suspicious=is_suspicious,
            description=desc,
        )

    def analyze_rgb(self, data: bytes) -> list[LSBDetectionResult]:
        results = []
        for i, channel in enumerate(["R", "G", "B"]):
            channel_data = data[i::3] if len(data) >= 3 else data
            results.append(self.analyze_channel(channel_data, channel))
        return results

    def get_suspicious_channels(self, results: list[LSBDetectionResult]) -> list[LSBDetectionResult]:
        return [r for r in results if r.is_suspicious]
