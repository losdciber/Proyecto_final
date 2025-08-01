def cargar_datos():
    url = "https://raw.githubusercontent.com/WuCandice/Superstore-Sales-Analysis/refs/heads/main/dataset/Superstore%20Dataset.csv
    data = pd. read_csv(ur1, encoding='latin1')
    data[ 'Order Date'] = pd. to_datetime(data] 'Order Date'])
    return data
df = cargar_datos()

st.sidebar.header("Filtros del Dashboard")
min_date = df['Order Date].min()
max_date = f}df['Order Date'].max()
fecha_inicial, fecha_final = st.sidebar.date_input(
    "Selecciona un rango de fechas ",
    value=[min_date, max_date]
    min_value=min_date
    max_value=max_date
)
df_filtrado = df[(df['Order Date'].between(pd.fecha_inicial, pd.fecha_final))]

st.title("Dashboard de Ventas de Superstore")
st.markdown('##')

ventas_totales = df['Sales'].sum()
utilidad_total = df['Profit'].sum()
ordenes_totales = df['order ID'].nunique()
clientes_totales = df['Customer ID'].nunique()

col1, col2, col3, col4 =st.columns(4)
whith col1:
    st.metric(label="Ventas Totales", value=f"${ventas_totales:,.2f}")
whith col2:
    st.metric(label="Utilidad Total", value=f"${utilidad_total:,.2f}")
whith col3:
    st.metric(label="Odenes Totales", value=f"${ordenes_totales:,.2f}")
whith col4:
    st.metric(label="Clientes Totales", value=f"${clientes_totales:,.2f}")

st.header("ventas y utilidades a lo largo del tiempo")
ventas_por_utilidad = df_filtrado.set_index('Order Date').resample('M').agg({'Sales': 'sum', 'Profit': 'sum'})

fig_area = px.area(
    ventas_por_utilidad,
    x='order_date',
    y=['Sales','Profit'],
    title=("Evolucion de ventas y utilidasdes en el tiempo"
    )

st.ploty_chart(fig_area, use_container_width=True)

st.markdown('---')
colpie, coldona =st.columns(2)

with colpie:
    ventas_by_region=df_filtrado.groupby('Region')['Sales'].sum().reset_index()
    fig_pie_region,
    names='Region',
    values='Sales',
    title='Ventas por Region',
)

st.plotly_chart(fig_pie_region, use_container_width=True)   