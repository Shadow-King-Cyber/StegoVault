"""Constructor de reportes de esteganografía."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ReportData:
    """Datos para generar un reporte esteganográfico."""
    filename: str
    file_format: str
    total_findings: int
    risk_level: str
    risk_score: int
    owasp_mapping: dict[str, str]
    entries: list[dict[str, Any]] = field(default_factory=list)


class ReportBuilder:
    """Construye reportes consolidados de análisis esteganográfico."""

    def build_summary(self, entries: list[dict[str, Any]]) -> dict[str, Any]:
        if not entries:
            return {"total": 0, "analysis_types": [], "risk_level": "Limpio"}

        analysis_types = list({e.get("analysis_type", "") for e in entries if e.get("analysis_type")})

        return {
            "total": len(entries),
            "analysis_types": analysis_types,
        }

    def build_report(self, data: ReportData) -> dict[str, Any]:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": "StegoVault",
            "version": "1.0.0",
            "filename": data.filename,
            "file_format": data.file_format,
            "summary": {
                "total_findings": data.total_findings,
                "risk_level": data.risk_level,
                "risk_score": data.risk_score,
            },
            "owasp_mapping": data.owasp_mapping,
            "entries": data.entries,
        }
