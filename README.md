# StegoVault

Herramienta de análisis de esteganografía para detectar y extraer datos ocultos en archivos.

> **ADVERTENCIA**: Solo para análisis forense autorizado. No usar para ocultar datos maliciosos.

## Características

- **Detección LSB** — Análisis de bits menos significativos en imágenes
- **Detección de metadatos** — EXIF, XMP, IPTC ocultos
- **Análisis de entropía** — Detección de regiones con alta entropía
- **Extracción de datos** — Extracción de bits ocultos en imagen
- **Detección de watermark** — Búsqueda de marcas de agua digitales
- **Análisis de consistencia** — Verificación de firmas de archivo y datos trailing
- **Scoring de riesgo** con mapeo OWASP
- **Reportes JSON + HTML** con visualizaciones
- **CLI Click** completo

## Aviso Legal

Esta herramienta se proporciona únicamente con fines educativos y para análisis forense autorizado. El usuario asume toda la responsabilidad de garantizar que cuenta con la autorización adecuada.

**Al usar este software, aceptas que:**
- Solo lo usarás con fines de aprendizaje o en investigaciones forenses autorizadas
- No usarás las técnicas implementadas para ocultar datos maliciosos
- Los autores no asumen responsabilidad por uso indebido

## Requisitos

- Python 3.11+

```bash
git clone https://github.com/Shadow-King-Cyber/StegoVault.git
cd StegoVault
pip install -r requirements.txt
```

## Inicio Rápido

```bash
# Análisis completo de un archivo
stego-vault analyze --file imagen.png

# Análisis de entropía
stego-vault entropy --file imagen.png

# Detectar metadatos ocultos
stego-vault metadata --file imagen.png

# Extraer datos ocultos (LSB)
stego-vault extract --file imagen.png

# Ver mapping OWASP
stego-vault mapping

# Generar reporte
stego-vault report
```

## Comandos del CLI

```bash
# Análisis completo
stego-vault analyze --file imagen.png

# Análisis de entropía
stego-vault entropy --file imagen.png

# Detectar metadatos ocultos
stego-vault metadata --file imagen.png

# Extraer datos ocultos
stego-vault extract --file imagen.png

# Ver mapping OWASP
stego-vault mapping

# Generar reporte HTML + JSON
stego-vault report
```

## Estructura del Proyecto

```
StegoVault/
├── stego_vault/
│   ├── core/           # AuditLogger
│   ├── analysis/       # EntropyAnalyzer, ConsistencyAnalyzer
│   ├── detection/      # LSBDetector, MetadataDetector, WatermarkDetector
│   ├── extraction/     # BitExtractor
│   ├── scoring/        # StegoScoring con OWASP mapping
│   ├── reporting/      # Reportes JSON/HTML
│   └── ui/             # CLI Click
├── tests/              # Suite de tests con pytest
├── requirements.txt    # Dependencias de Python
├── pyproject.toml      # Configuración del proyecto
└── LICENSE             # Licencia MIT
```

## Ejecutar Tests

```bash
pytest -v
```

## Licencia

MIT License — ver [LICENSE](LICENSE)
