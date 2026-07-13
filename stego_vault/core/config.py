"""Configuración global de StegoVault."""

from pathlib import Path


class Config:
    """Configuración centralizada."""

    BASE_DIR = Path(__file__).resolve().parent.parent
    SCOPE_FILE = BASE_DIR / "scope.json"
    AUDIT_LOG = BASE_DIR / "audit_log.jsonl"
    REPORTS_DIR = BASE_DIR / "reports"

    SUPPORTED_FORMATS = ["png", "jpeg", "jpg", "bmp", "wav", "mp3", "txt"]

    ENTROPY_THRESHOLD = 7.5
    LSB_ANALYSIS_BITS = 1

    STEGANOGRAPHY_SIGNATURES = {
        "LSB": "Baja entropía en bits menos significativos",
        "DCT": "Datos ocultos en coeficientes DCT (JPEG)",
        "Metadata": "Metadatos EXIF/XMP/IPTC sospechosos",
        "Watermark": "Marca de agua digital detectada",
        "FileAppending": "Datos adicionales al final del archivo",
    }

    OWASP_MAPPING = {
        "Data Hiding": "A08:2021 — Software and Data Integrity Failures",
        "Metadata Abuse": "A05:2021 — Security Misconfiguration",
        "Exfiltration": "A04:2021 — Insecure Design",
    }
