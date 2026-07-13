"""CLI principal para StegoVault."""

import click

from ..core.audit_logger import AuditLogger
from ..analysis.entropy_analyzer import EntropyAnalyzer
from ..analysis.consistency_analyzer import ConsistencyAnalyzer
from ..detection.lsb_detector import LSBDetector
from ..detection.metadata_detector import MetadataDetector
from ..detection.watermark_detector import WatermarkDetector
from ..extraction.bit_extractor import BitExtractor
from ..scoring.stego_scoring import StegoScoring
from ..reporting.report_builder import ReportBuilder, ReportData
from ..reporting.json_exporter import JsonExporter
from ..reporting.html_exporter import HtmlExporter


@click.group()
@click.version_option(version="1.0.0", prog_name="stego-vault")
def main() -> None:
    """StegoVault — Herramienta de análisis de esteganografía."""
    pass


@main.command()
@click.option("--file", required=True, help="Archivo a analizar")
def analyze(file: str) -> None:
    """Análisis completo de un archivo."""
    click.echo(f"=== Análisis esteganográfico: {file} ===")
    logger = AuditLogger()
    logger.log_analysis(file, "full_analysis", 0)
    click.echo("Análisis registrado. Use comandos individuales para detalles.")


@main.command()
@click.option("--file", required=True, help="Archivo a analizar")
def entropy(file: str) -> None:
    """Análisis de entropía del archivo."""
    analyzer = EntropyAnalyzer()
    with open(file, "rb") as f:
        data = f.read()
    results = analyzer.analyze_data(data, chunk_size=256)
    suspicious = analyzer.get_suspicious_regions(results)
    click.echo(f"=== Análisis de Entropía: {file} ===")
    click.echo(f"Chunks analizados: {len(results)}")
    click.echo(f"Sospechosos: {len(suspicious)}")
    for r in suspicious[:5]:
        click.echo(f"  [!] {r.region}: {r.description}")


@main.command()
@click.option("--file", required=True, help="Archivo a analizar")
def metadata(file: str) -> None:
    """Detecta metadatos ocultos."""
    detector = MetadataDetector()
    with open(file, "rb") as f:
        data = f.read()
    hidden = detector.scan_raw_data(data)
    click.echo(f"=== Detección de Metadatos: {file} ===")
    if hidden:
        for h in hidden:
            click.echo(f"  [!] {h}")
    else:
        click.echo("  [OK] No se detectaron metadatos ocultos")


@main.command()
@click.option("--file", required=True, help="Archivo a analizar")
def extract(file: str) -> None:
    """Extrae datos ocultos del archivo."""
    extractor = BitExtractor()
    with open(file, "rb") as f:
        data = f.read()
    result = extractor.extract_lsb_text(data)
    click.echo(f"=== Extracción LSB: {file} ===")
    click.echo(f"Método: {result.method}")
    click.echo(f"Bytes extraídos: {result.length}")
    if result.extracted_text:
        click.echo(f"Texto:\n{result.extracted_text[:500]}")
    else:
        click.echo("No se detectó texto legible")


@main.command()
def mapping() -> None:
    """Muestra el mapping OWASP para esteganografía."""
    scoring = StegoScoring()
    mappings = scoring.get_owasp_mapping()
    click.echo("=== OWASP Mapping ===\n")
    for k, v in mappings.items():
        click.echo(f"  {k}: {v}")


@main.command()
def report() -> None:
    """Genera un reporte HTML + JSON."""
    logger = AuditLogger()
    entries = logger.read_all()
    builder = ReportBuilder()
    summary = builder.build_summary(entries)

    scoring = StegoScoring()
    score_result = scoring.calculate_score([e.get("analysis_type", "") for e in entries])

    data = ReportData(
        filename="N/A",
        file_format="N/A",
        total_findings=summary.get("total", 0),
        risk_level=score_result.risk_level,
        risk_score=score_result.score,
        owasp_mapping=scoring.get_owasp_mapping(),
        entries=entries,
    )
    report_data = builder.build_report(data)

    json_exp = JsonExporter()
    json_path = json_exp.export(report_data)
    click.echo(f"Reporte JSON: {json_path}")

    html_exp = HtmlExporter()
    html_path = html_exp.export(report_data)
    click.echo(f"Reporte HTML: {html_path}")
    click.echo(f"\nNivel de riesgo: {score_result.risk_level} (Score: {score_result.score}/10)")


if __name__ == "__main__":
    main()
