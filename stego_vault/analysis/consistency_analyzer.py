"""Analizador de consistencia de archivos."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConsistencyResult:
    """Resultado de análisis de consistencia."""
    check: str
    is_consistent: bool
    severity: str
    description: str


class ConsistencyAnalyzer:
    """Verifica la consistencia estructural de archivos."""

    FILE_SIGNATURES = {
        b"\x89PNG": "PNG",
        b"\xff\xd8\xff": "JPEG",
        b"BM": "BMP",
        b"RIFF": "WAV",
        b"ID3": "MP3",
    }

    def check_file_signature(self, data: bytes, expected_format: str) -> ConsistencyResult:
        detected = None
        for sig, fmt in self.FILE_SIGNATURES.items():
            if data[:len(sig)] == sig:
                detected = fmt
                break

        if detected is None:
            return ConsistencyResult(
                check="file_signature",
                is_consistent=False,
                severity="Alto",
                description="Firma de archivo no reconocida",
            )

        is_match = detected.lower() == expected_format.lower().replace("jpg", "jpeg")
        return ConsistencyResult(
            check="file_signature",
            is_consistent=is_match,
            severity="OK" if is_match else "Alto",
            description=f"Detectado: {detected} (esperado: {expected_format})" if not is_match else f"Formato correcto: {detected}",
        )

    def check_file_size(self, data: bytes, min_size: int = 100, max_size: int = 100_000_000) -> ConsistencyResult:
        size = len(data)
        if size < min_size:
            return ConsistencyResult(
                check="file_size",
                is_consistent=False,
                severity="Medio",
                description=f"Archivo muy pequeño ({size} bytes)",
            )
        if size > max_size:
            return ConsistencyResult(
                check="file_size",
                is_consistent=False,
                severity="Medio",
                description=f"Archivo muy grande ({size} bytes)",
            )
        return ConsistencyResult(
            check="file_size",
            is_consistent=True,
            severity="OK",
            description=f"Tamaño normal ({size} bytes)",
        )

    def check_trailing_data(self, data: bytes, format_end_marker: bytes | None = None) -> ConsistencyResult:
        if format_end_marker and data.endswith(format_end_marker):
            return ConsistencyResult(
                check="trailing_data",
                is_consistent=True,
                severity="OK",
                description="No se detectaron datos adicionales al final",
            )

        trailing_zeros = 0
        for byte in reversed(data):
            if byte == 0:
                trailing_zeros += 1
            else:
                break

        if trailing_zeros > 1024:
            return ConsistencyResult(
                check="trailing_data",
                is_consistent=False,
                severity="Medio",
                description=f"{trailing_zeros} bytes nulos al final del archivo — posible dato oculto",
            )

        return ConsistencyResult(
            check="trailing_data",
            is_consistent=True,
            severity="OK",
            description="Sin trailing data sospechoso",
        )

    def run_all_checks(self, data: bytes, file_format: str) -> list[ConsistencyResult]:
        results = [
            self.check_file_signature(data, file_format),
            self.check_file_size(data),
            self.check_trailing_data(data),
        ]
        return results

    def get_inconsistent(self, results: list[ConsistencyResult]) -> list[ConsistencyResult]:
        return [r for r in results if not r.is_consistent]
