"""Detector de marcas de agua digitales."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WatermarkResult:
    """Resultado de detección de watermark."""
    watermark_type: str
    detected: bool
    confidence: float
    description: str


class WatermarkDetector:
    """Detecta marcas de agua digitales en archivos."""

    WATERMARK_MARKERS = {
        b"wm_": "Watermark marker",
        b"DGMC": "Digimarc",
        b"WTMK": "Visible watermark",
        b"\x00W\x00M": "Unicode watermark",
    }

    def detect_watermark(self, data: bytes) -> list[WatermarkResult]:
        results = []
        for marker, wtype in self.WATERMARK_MARKERS.items():
            if marker in data:
                results.append(WatermarkResult(
                    watermark_type=wtype,
                    detected=True,
                    confidence=0.8,
                    description=f"Marcador de watermark '{wtype}' encontrado",
                ))
        return results

    def detect_repeated_patterns(self, data: bytes, pattern_size: int = 16) -> WatermarkResult | None:
        if len(data) < pattern_size * 4:
            return None

        patterns = {}
        for i in range(0, len(data) - pattern_size, pattern_size):
            chunk = data[i:i + pattern_size]
            patterns[chunk] = patterns.get(chunk, 0) + 1

        most_common = max(patterns.items(), key=lambda x: x[1])
        if most_common[1] >= 4:
            return WatermarkResult(
                watermark_type="Repeated pattern",
                detected=True,
                confidence=min(0.9, most_common[1] * 0.1),
                description=f"Patrón repetido {most_common[1]} veces — posible watermark",
            )
        return None

    def analyze(self, data: bytes) -> list[WatermarkResult]:
        results = self.detect_watermark(data)
        pattern = self.detect_repeated_patterns(data)
        if pattern:
            results.append(pattern)
        return results

    def get_detected(self, results: list[WatermarkResult]) -> list[WatermarkResult]:
        return [r for r in results if r.detected]
