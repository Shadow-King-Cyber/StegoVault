"""Gestión de scope para análisis de esteganografía."""

import json
from pathlib import Path
from typing import Any


class ScopeManager:
    """Gestiona el alcance autorizado del análisis."""

    def __init__(self, scope_path: str | Path = "scope.json") -> None:
        self._scope_path = Path(scope_path)
        self._scope = self._load_scope()

    def _load_scope(self) -> dict[str, Any]:
        if self._scope_path.exists():
            return json.loads(self._scope_path.read_text(encoding="utf-8"))
        return {"authorized": False, "files": [], "purpose": "", "operator": ""}

    def save(self) -> None:
        self._scope_path.write_text(
            json.dumps(self._scope, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def is_authorized(self) -> bool:
        return self._scope.get("authorized", False)

    def get_files(self) -> list[str]:
        return self._scope.get("files", [])

    def set_authorized(self, authorized: bool) -> None:
        self._scope["authorized"] = authorized

    def set_files(self, files: list[str]) -> None:
        self._scope["files"] = files

    def require_authorization(self) -> None:
        if not self.is_authorized():
            raise PermissionError(
                "Análisis no autorizado. Configure scope.json con authorized: true"
            )
