"""Analizador de entropía para detección de datos ocultos."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass


@dataclass
class EntropyResult:
    """Resultado de análisis de entropía."""
    region: str
    entropy: float
    is_suspicious: bool
    description: str


class EntropyAnalyzer:
    """Analiza la entropía de datos para detectar patrones inusuales."""

    SUSPICIOUS_THRESHOLD = 7.5
    RANDOM_THRESHOLD = 7.9

    def calculate_entropy(self, data: bytes) -> float:
        if not data:
            return 0.0
        counter = Counter(data)
        length = len(data)
        entropy = 0.0
        for count in counter.values():
            p = count / length
            if p > 0:
                entropy -= p * math.log2(p)
        return round(entropy, 4)

    def analyze_region(self, data: bytes, region_name: str) -> EntropyResult:
        entropy = self.calculate_entropy(data)
        is_suspicious = entropy >= self.SUSPICIOUS_THRESHOLD
        is_random = entropy >= self.RANDOM_THRESHOLD

        if is_random:
            desc = f"Entropía muy alta ({entropy}) — posible cifrado o compresión"
        elif is_suspicious:
            desc = f"Entropía alta ({entropy}) — posible dato oculto"
        else:
            desc = f"Entropía normal ({entropy})"

        return EntropyResult(
            region=region_name,
            entropy=entropy,
            is_suspicious=is_suspicious,
            description=desc,
        )

    def analyze_data(self, data: bytes, chunk_size: int = 1024) -> list[EntropyResult]:
        results = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            region = f"chunk_{i // chunk_size}"
            results.append(self.analyze_region(chunk, region))
        return results

    def get_suspicious_regions(self, results: list[EntropyResult]) -> list[EntropyResult]:
        return [r for r in results if r.is_suspicious]
