"""Detector de metadatos ocultos (EXIF, XMP, IPTC)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MetadataDetectionResult:
    """Resultado de detección de metadatos."""
    metadata_type: str
    fields_found: int
    suspicious_fields: list[str]
    is_suspicious: bool
    description: str


class MetadataDetector:
    """Detecta metadatos ocultos o sospechosos en archivos."""

    SUSPICIOUS_FIELDS = [
        "Comment", "UserComment", "ImageDescription",
        "XPAuthor", "XPComment", "XPTitle",
        "Copyright", "Artist", "Software",
    ]

    KNOWN_SIGNATURES = {
        b"Exif": "EXIF",
        b"http://ns.adobe.com/xap": "XMP",
        b"IPTC": "IPTC",
    }

    def detect_signatures(self, data: bytes) -> list[str]:
        found = []
        for sig, name in self.KNOWN_SIGNATURES.items():
            if sig in data:
                found.append(name)
        return found

    def analyze_metadata(self, metadata: dict, metadata_type: str = "EXIF") -> MetadataDetectionResult:
        suspicious = []
        for key, value in metadata.items():
            if key in self.SUSPICIOUS_FIELDS and value:
                suspicious.append(f"{key}: {str(value)[:50]}")

        return MetadataDetectionResult(
            metadata_type=metadata_type,
            fields_found=len(metadata),
            suspicious_fields=suspicious,
            is_suspicious=len(suspicious) > 0,
            description=f"Metadatos {metadata_type}: {len(metadata)} campos, {len(suspicious)} sospechosos",
        )

    def scan_raw_data(self, data: bytes) -> list[str]:
        hidden = []
        for raw_sig, name in self.KNOWN_SIGNATURES.items():
            if raw_sig in data:
                idx = data.find(raw_sig)
                if idx >= 0:
                    hidden.append(f"{name} encontrado en offset {idx}")
        return hidden

    def get_suspicious_findings(self, results: list[MetadataDetectionResult]) -> list[MetadataDetectionResult]:
        return [r for r in results if r.is_suspicious]
