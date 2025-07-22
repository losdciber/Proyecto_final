# Dashboard Energético con Streamlit

Este proyecto muestra un dashboard interactivo de análisis energético con datos de electricidad mensual.

## Estructura

- `app.py`: archivo principal que lanza la aplicación.
- `utils.py`: funciones reutilizables (carga de datos, clasificación, filtros).
- `secciones/`: contiene las distintas secciones del dashboard.
- `data/`: base de datos SQLite `analisis_energetico.db`.

## Requisitos

Instala dependencias con:

```bash
pip install -r requirements.txt
```

## Ejecución local

```bash
streamlit run app.py
```

## Despliegue en Railway

1. Subir el proyecto a GitHub.
2. Crear nuevo proyecto en Railway y conectarlo a tu repo.
3. Railway instalará automáticamente las dependencias y ejecutará `app.py`.

