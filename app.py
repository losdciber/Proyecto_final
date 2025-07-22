import streamlit as st
from utils import cargar_datos
from secciones import (
    home,
    matriz_energetica,
    consumo_energetico,
    matriz_electrica,
    comparativos_internacionales,
    emisiones_co2,
    relaciones_desempeno,
    predicciones,
    flujos_energeticos
)

# Configurar la página
st.set_page_config(page_title="Dashboard Energético", layout="wide")

# Cargar datos una sola vez
df = cargar_datos()

# Estilos CSS personalizados para el sidebar (modo claro)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f2f2f2;
    }
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #000000;
        padding-bottom: 10px;
    }
    .sidebar-radio label {
        font-size: 18px;
        padding: 8px 12px;
        border-radius: 6px;
        display: block;
        margin-bottom: 5px;
        color: #000000;
        transition: background-color 0.3s ease;
    }
    .sidebar-radio label:hover {
        background-color: #d6d6d6;
        color: #000000;
    }
    .sidebar-radio input:checked + div {
        background-color: #cccccc !important;
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar: navegación mejorada sin emojis
menu_opciones = {
    "Home": "Home",
    "Matriz Energética": "Matriz Energética",
    "Consumo Energético": "Consumo Energético",
    "Matriz Eléctrica": "Matriz Eléctrica",
    "Comparativos Internacionales": "Comparativos Internacionales",
    "Emisiones de CO2": "Emisiones de CO2",
    "Análisis de Relaciones y Desempeño": "Análisis de Relaciones y Desempeño",
    "Predicciones": "Predicciones",
    "Flujos Energéticos": "Flujos Energéticos"
}

with st.sidebar:
    st.markdown('<div class="sidebar-title">Menú de navegación</div>', unsafe_allow_html=True)
    seccion = st.radio(
        "",
        list(menu_opciones.keys()),
        format_func=lambda x: menu_opciones[x],
        key="navegacion"
    )

# Navegación por sección
if seccion == "Home":
    home.mostrar()
elif seccion == "Matriz Energética":
    matriz_energetica.mostrar(df)
elif seccion == "Consumo Energético":
    consumo_energetico.mostrar(df)
elif seccion == "Matriz Eléctrica":
    matriz_electrica.mostrar(df)
elif seccion == "Comparativos Internacionales":
    comparativos_internacionales.mostrar(df)
elif seccion == "Emisiones de CO2":
    emisiones_co2.mostrar(df)
elif seccion == "Análisis de Relaciones y Desempeño":
    relaciones_desempeno.mostrar(df)
elif seccion == "Predicciones":
    predicciones.mostrar()
elif seccion == "Flujos Energéticos":
    flujos_energeticos.mostrar()
