
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

def ejecutar_consulta(query):
    """
    Ejecuta una consulta SQL en la base de datos 'analisis_energetico.db' y devuelve un DataFrame.

    Parámetros:
    - query: Cadena de texto con la consulta SQL.

    Retorna:
    - DataFrame con el resultado de la consulta.
    """
    conn = sqlite3.connect("data/analisis_energetico.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def cargar_datos():
    """
    Carga toda la tabla 'Monthly_Electricity_Statistics' desde la base de datos SQLite,
    excluyendo registros globales o promedios agregados como "OECD" o "Total", y agrega
    una columna de año (Year) para facilitar análisis anuales.

    Retorna:
    - DataFrame con los datos filtrados y columna adicional 'Year'.
    """
    query = """
    SELECT * 
    FROM 'Monthly_Electricity_Statistics'
    WHERE Country NOT LIKE '%OECD%' 
      AND Country NOT LIKE '%Total%'
    ORDER BY Country ASC
    """
    df = ejecutar_consulta(query)
    df['Year'] = df['Time'].str.extract(r'(\d{4})')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype('Int64')
    return df

def obtener_produccion_mensual():
    """
    Consultar la base de datos para obtener únicamente los registros donde
    el balance sea 'Net Electricity Production'. Devuelve columnas clave
    como Product, Country, Time, Value y Balance.

    Retorna:
    - DataFrame con datos de producción neta de electricidad.
    """
    query = """
    SELECT Product, Country, Time, Value, Balance
    FROM Monthly_Electricity_Statistics
    WHERE Balance = 'Net Electricity Production'
    """
    return ejecutar_consulta(query)

def clasificar_y_filtrar_productos(df, pais=None, tipo_energia='ambas'):
    """
    Clasifica cada fila del DataFrame según el tipo de energía (renovable o no renovable)
    y aplica filtros opcionales por país y tipo de energía.

    Parámetros:
    - df: DataFrame con columnas 'Product', 'Country', 'Value', etc.
    - pais: Nombre del país a filtrar (por defecto: None o 'Todos')
    - tipo_energia: 'ambas', 'renovables' o 'no_renovables'

    Retorna:
    - DataFrame filtrado y clasificado, con columna extra 'Energy_Type'.
    """
    productos_excluir = [
        'Electricity', 'Total Combustible Fuels',
        'Total Renewables (Hydro, Geo, Solar, Wind, Other)',
        'Not Specified', 'Data is estimated for this month'
    ]
    productos_renovables = [
        'Hydro', 'Wind', 'Geothermal',
        'Combustible Renewables', 'Solar', 'Other Renewables'
    ]
    df_filtrado = df[~df['Product'].isin(productos_excluir)].copy()
    df_filtrado['Energy_Type'] = df_filtrado['Product'].apply(
        lambda x: 'Renewable' if x in productos_renovables else 'Non-Renewable'
    )
    if pais and pais != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Country'] == pais]
    if tipo_energia == 'renovables':
        df_filtrado = df_filtrado[df_filtrado['Energy_Type'] == 'Renewable']
    elif tipo_energia == 'no_renovables':
        df_filtrado = df_filtrado[df_filtrado['Energy_Type'] == 'Non-Renewable']
    return df_filtrado

def obtener_emisiones_co2():
    """
    Carga los datos de emisiones de CO₂ desde la tabla:
    'International Energy Agency - CO2 emissions by sector in Colombia'
    """
    query = 'SELECT * FROM "International Energy Agency - CO2 emissions by sector in Colombia"'
    return ejecutar_consulta(query)


def obtener_datos_corr_emisiones_y_generacion():
    """
    Obtiene los datos necesarios para calcular la correlación entre:
    - Emisiones por combustibles fósiles
    - Generación eléctrica por carbón
    - Generación eléctrica por gas

    Retorna:
    - DataFrame con columnas: Year, EmisionesFosiles, GeneracionCarbon, GeneracionGas
    """
    query = """
    SELECT 
        e.Year AS Year,
        e.Fuel AS EmisionesFosiles,
        c."Electricity generation from coal, Colombia" AS GeneracionCarbon,
        g."Electricity generation from gas, Colombia" AS GeneracionGas
    FROM "International Energy Agency - CO2 emissions from fuel combustion, Colombia" e
    JOIN "International Energy Agency - Electricity generation from coal, Colombia" c ON e.Year = c.Year
    JOIN "International Energy Agency - Electricity generation from gas, Colombia" g ON e.Year = g.Year
    ORDER BY e.Year
    """
    return ejecutar_consulta(query)

def mostrar_tarjeta_valor_maximo(df, campo_clave, campo_valor, titulo, unidad="", color="#1F4E79"):
    if not df.empty:
        fila_max = df.loc[df[campo_valor].idxmax()]
        valor = fila_max[campo_valor]
        clave = fila_max[campo_clave]

        st.markdown(
            f"""
            <div style='padding: 0.5em; background-color: #f0f2f6; border-left: 6px solid {color}; border-radius: 8px; margin-bottom: 0.5em;'>
                <h4 style='color: {color};'> {titulo}</h4>
                <p style='font-size: 24px;'><strong>{clave}</strong>: {valor:.2f} {unidad}</p>
            </div>
            """, unsafe_allow_html=True
        )
        
def mostrar_tabla_y_barras_lado_a_lado(df, campo_categoria, campo_valor, titulo="", unidad="MtCO₂", color="salmon"):
    """
    Muestra una tabla con los valores y al lado derecho un gráfico de barras horizontal con la participación porcentual.
    
    Parámetros:
    - df: DataFrame ya filtrado y ordenado
    - campo_categoria: nombre de la columna con las categorías (ej. "Sector")
    - campo_valor: nombre de la columna con los valores (ej. "Value")
    - titulo: título opcional para la sección
    - unidad: unidad que se muestra en la tabla (por defecto "MtCO₂")
    - color: color de las barras (por defecto "salmon")
    """

    if titulo:
        st.markdown(f"### {titulo}")

    # Calcular participación
    total = df[campo_valor].sum()
    df['Porcentaje'] = df[campo_valor] / total * 100
    df = df.sort_values(by=campo_valor, ascending=False).reset_index(drop=True)

    col1, col2 = st.columns([1, 1.5])

    with col1:
        tabla = df[[campo_categoria, campo_valor]].copy()
        tabla.columns = ["Categoría", f"{unidad}"]
        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True,
            height=(len(df) * 35 + 50)
        )

    with col2:
        df['Etiqueta'] = df['Porcentaje'].apply(lambda x: f"{x:.1f}%")
        fig = px.bar(
            df,
            x="Porcentaje",
            y=campo_categoria,
            orientation="h",
            text="Etiqueta",
            color_discrete_sequence=[color]
        )
        fig.update_layout(
            title=None,
            xaxis_title=None,
            yaxis_title=None,
            yaxis=dict(showticklabels=False, categoryorder='total ascending'),
            xaxis=dict(showticklabels=False),
            margin=dict(l=10, r=10, t=10, b=10),
            height=(len(df) * 35 + 50),
            uniformtext_minsize=8,
            uniformtext_mode='show',
        )
        st.plotly_chart(fig, use_container_width=True)
