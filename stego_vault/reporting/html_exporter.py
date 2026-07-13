"""Exportación de reportes a HTML con Chart.js."""

from pathlib import Path
from typing import Any


class HtmlExporter:
    """Exporta reportes esteganográficos a HTML con gráficos Chart.js."""

    def __init__(self, output_dir: str | Path = "reports") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, data: dict[str, Any], filename: str = "report.html") -> Path:
        summary = data.get("summary", {})
        risk_level = summary.get("risk_level", "Limpio")

        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>StegoVault — Reporte</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {{ font-family: monospace; background: #0a0a0a; color: #00ff41; padding: 20px; }}
h1 {{ color: #ff4444; }}
canvas {{ max-width: 500px; margin: 20px 0; }}
table {{ border-collapse: collapse; margin: 10px 0; }}
td, th {{ border: 1px solid #00ff41; padding: 8px; }}
.risk {{ font-size: 24px; font-weight: bold; }}
.risk.critico {{ color: #ff0000; }}
.risk.alto {{ color: #ff4444; }}
.risk.medio {{ color: #ffaa00; }}
.risk.limpio {{ color: #00ff41; }}
</style>
</head>
<body>
<h1>StegoVault — Reporte de Esteganografía</h1>
<p>Archivo: <strong>{data.get('filename', 'N/A')}</strong></p>
<p>Riesgo: <span class="risk {risk_level.lower()}">{risk_level}</span></p>
<p>Score: <strong>{summary.get('risk_score', 0)}/10</strong></p>
<p>Findings: <strong>{summary.get('total_findings', 0)}</strong></p>
<h2>OWASP Mapping</h2>
<table>
<tr><th>Tipo</th><th>Referencia</th></tr>
{"".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in data.get('owasp_mapping', {}).items())}
</table>
<script>
new Chart(document.getElementById('riskChart'), {{
  type: 'doughnut',
  data: {{
    labels: ['High', 'Medium', 'Low'],
    datasets: [{{data: [{summary.get('total_findings', 0)}, 0, 0], backgroundColor: ['#ff4444','#ffaa00','#00ff41']}}]
  }}
}});
</script>
</body>
</html>"""

        output = self._output_dir / filename
        output.write_text(html, encoding="utf-8")
        return output
