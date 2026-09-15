# Currículum del portfolio

El PDF público es `public/CV_Javi_Paez.pdf`. Astro lo copia a `dist/` al compilar
y el despliegue existente lo publica en https://portfolio.javistudio.dev/CV_Javi_Paez.pdf.

## Fuente editable y generación

El texto y la maquetación están en `scripts/cv.py`; la fotografía es
`public/javi-paez.jpg`. El generador se reconstruyó el 15 de septiembre de 2026
a partir del PDF anterior: no es el script original recuperado.

Requiere Python 3 y las dependencias fijadas en `scripts/requirements-cv.txt`.
Usa las fuentes Bitstream Vera incluidas en ReportLab, sin depender de Segoe UI
ni copiar fuentes propietarias de Windows a la VPS.

```sh
python -m venv .venv-cv
# Linux: source .venv-cv/bin/activate
# PowerShell: .\.venv-cv\Scripts\Activate.ps1
python -m pip install -r scripts/requirements-cv.txt
python scripts/cv.py
python -m unittest discover -s scripts -p test_cv.py
npm run build
```

También se puede generar una propuesta sin sobrescribir el PDF del repositorio:

```sh
python scripts/cv.py --output /ruta/a/propuesta.pdf
```

Antes de publicar, abrir el PDF y revisar la página completa, acentos, fotografía,
columnas y enlaces. Las pruebas comprueban una página, texto esperado, enlaces,
ausencia de los errores corregidos y generación repetible en el mismo entorno.
El generador detiene la ejecución si el contenido supera el margen inferior.
Los metadatos de fecha son fijos por la opción de generación determinista;
la fecha real de una modificación debe consultarse en Git.

Versionar juntos el generador y el PDF actualizado. El flujo existente despliega
al hacer push a `master`; no ejecuta Python automáticamente. Un cambio solo en
el generador no actualiza por sí mismo el PDF servido.

## Corrección del 15 de septiembre de 2026

- Corregido el literal `D&D;` a `D&D`.
- Sustituida la mención a Supabase en proyectos independientes por PostgreSQL,
  coherente con la corrección ya aplicada al portfolio en `bc56b93`.
- Sustituido Supabase por PocketBase en la sección Datos y explicitado PocketBase
  en DM Command, cuya persistencia ya estaba verificada en la VPS.
- Conservados nombre, contacto, fechas, formación y experiencia del documento previo.
- Mantenida la composición de una página con cabecera, fotografía y dos columnas;
  cambia la tipografía para permitir regeneración sin fuentes del sistema.

No se deduce de estas correcciones que Javier nunca haya usado Supabase: se alinea
este documento con los proyectos y el texto actual del portfolio.
