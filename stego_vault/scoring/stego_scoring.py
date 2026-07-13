"""Scoring de riesgo de esteganografía."""

from dataclasses import dataclass


@dataclass
class StegoScore:
    """Resultado de scoring esteganográfico."""
    total_findings: int
    high_risk: int
    medium_risk: int
    low_risk: int
    risk_level: str
    score: int


class StegoScoring:
    """Calcula el nivel de riesgo de esteganografía."""

    RISK_WEIGHTS = {
        "LSB": 3,
        "Metadata": 2,
        "Watermark": 1,
        "FileAppending": 2,
        "DCT": 3,
    }

    RISK_LEVELS = [
        (8, "Crítico"),
        (5, "Alto"),
        (3, "Medio"),
        (1, "Bajo"),
        (0, "Limpio"),
    ]

    def calculate_score(self, findings: list[str]) -> StegoScore:
        total_score = 0
        for finding in findings:
            for method, weight in self.RISK_WEIGHTS.items():
                if method.lower() in finding.lower():
                    total_score += weight
                    break

        high = sum(1 for f in findings if any(m in f.lower() for m in ["lsb", "dct"]))
        medium = sum(1 for f in findings if any(m in f.lower() for m in ["metadata", "fileappending"]))
        low = sum(1 for f in findings if "watermark" in f.lower())

        risk_level = "Limpio"
        for threshold, level in self.RISK_LEVELS:
            if total_score >= threshold:
                risk_level = level
                break

        return StegoScore(
            total_findings=len(findings),
            high_risk=high,
            medium_risk=medium,
            low_risk=low,
            risk_level=risk_level,
            score=min(10, total_score),
        )

    def get_owasp_mapping(self) -> dict[str, str]:
        return {
            "Data Hiding": "A08:2021 — Software and Data Integrity Failures",
            "Metadata Abuse": "A05:2021 — Security Misconfiguration",
            "Exfiltration": "A04:2021 — Insecure Design",
        }
