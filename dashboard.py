def cargar_datos():
    url = "https://github.com/WuCandice/Superstore-Sales-Analysis/blob/65d5997da060141a282982bb03ddcf4629431a40/dataset/Superstore%20Dataset.csv
    data = pd. read_csv(ur1, encoding='latin1')
    data[ 'Order Date'] = pd. to_datetime(data] 'Order Date'])
    return data
df = cargar_datos()

st.sidebar.header("Filtros del Dashboard")
min_date = df['Order Date].min()
max_date = f}df['Order Date'].max()
fecha_inicial, fecha_final = st.sidebar.date_input(
    "Selecciona un rango de fechas ",
    min_value=min_date
    max_value=max_date
)
df_filtrado = df[(df['Order Date'].between(pd.fecha_inicial, pd.fecha_final))]

st.title("Dashboard de Ventas de Superstore")
st.markdown('##')

ventas_total = df['Sales'].sum()
utilidad_total = df['Profit'].sum()
ordenes_totales = df['order ID'].nunique()
clientes_totales = df['Customer ID'].nunique()

col1, col2, col3, col4 =st.columns(4)
whith col1:
    st.metric(label="Ventas Totales", value=f"${ventas_total:,.2f}")