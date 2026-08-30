# Xolos Dashboard

Dashboard de jugadores prestados de Xoloitzcuintles.

- `update_dashboard.py`: obtiene los datos de las fuentes configuradas y genera `index.html`.
- `SOFASCORE_MANUAL`: valores manuales de MP, MIN, GLS y AST para los cuatro jugadores de SofaScore.
- `.github/workflows/update-dashboard.yml`: actualiza y publica el dashboard cada lunes a las 07:00 (America/Tijuana), y permite ejecución manual.
