import subprocess
import time
from pyngrok import ngrok
import os

# Ruta a streamlit dentro del entorno virtual
streamlit_path = r"C:\Entrega Final\Analitica_talento_tech\.venv\Scripts\streamlit.exe"

# Ruta a tu app
app_path = r"C:\Entrega Final\Analitica_talento_tech\app.py"

# Cambiar al directorio donde está la app
os.chdir(os.path.dirname(app_path))

# Ejecutar Streamlit
subprocess.Popen([streamlit_path, "run", "app.py"])
time.sleep(5)

# Exponer con ngrok
public_url = ngrok.connect(8501)
print("🌍 Tu app está disponible públicamente en:", public_url)
