@echo off
cd /d "C:\Entrega Final\Analitica_talento_tech"

echo Activando entorno virtual...
call .venv\Scripts\activate

:: Registrar token de ngrok (puedes comentar esta línea después de la primera vez)
echo Registrando Authtoken de ngrok...
python registrar_token.py

echo Lanzando Streamlit y Ngrok...
python exponer.py

pause
