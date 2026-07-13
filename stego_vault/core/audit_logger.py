"""Auditoría de operaciones de análisis."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class AuditLogger:
    """Registra todas las operaciones de análisis esteganográfico."""

    def __init__(self, log_path: str | Path = "audit_log.jsonl") -> None:
        self._log_path = Path(log_path)

    def log(self, event_type: str, details: dict[str, Any]) -> None:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details,
        }
        with open(self._log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_analysis(self, filename: str, analysis_type: str, findings: int) -> None:
        self.log("analysis_completed", {
            "filename": filename,
            "analysis_type": analysis_type,
            "findings": findings,
        })

    def read_all(self) -> list[dict[str, Any]]:
        if not self._log_path.exists():
            return []
        entries = []
        with open(self._log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries
