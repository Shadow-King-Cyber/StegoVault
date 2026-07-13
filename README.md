# StegoVault

Herramienta de análisis de esteganografía para detectar y extraer datos ocultos en archivos.

> **ADVERTENCIA**: Solo para análisis forense autorizado. No usar para ocultar datos maliciosos.

## Características

- **Detección LSB** — Análisis de bits menos significativos en imágenes
- **Detección de metadatos** — EXIF, XMP, IPTC ocultos
- **Análisis de entropía** — Detección de regiones con alta entropía
- **Extracción de datos** — Extracción de bits ocultos
- **Detección de watermark** — Búsqueda de marcas de agua digitales
- **Análisis de archivos** — PNG, JPEG, BMP, WAV, MP3
- **CLI Click** completo
- **Reportes JSON + HTML** con Chart.js
- **OWASP mapping** para datos ocultos

## Instalación

```bash
git clone https://github.com/Shadow-King-Cyber/StegoVault.git
cd StegoVault
pip install -r requirements.txt
```

## Uso

```bash
# Analizar imagen
stego-vault analyze --file imagen.png

# Extraer datos ocultos
stego-vault extract --file imagen.png

# Análisis de entropía
stego-vault entropy --file imagen.png

# Detectar metadatos ocultos
stego-vault metadata --file imagen.png

# Generar reporte
stego-vault report
```

## Licencia

MIT License — Shadow-King-Cyber
