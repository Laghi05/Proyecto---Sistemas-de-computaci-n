# Importacion de librerias
import pyodbc
import pip
import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib
import os
import warnings
warnings.filterwarnings('ignore')

############################################################################################

#Conexión con la base de datos alojada en SQL SERVER

host = "DESKTOP-DH1O5F3"
user = "Grupo-C"
password = "123456"
database = "BD_VIH"

def conexionDB():
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                                  'SERVER=' + host + ';'
                                  'DATABASE=' + database + ';'
                                  'UID=' + user + ';'
                                  'PWD=' + password + ';'
                                  'TrustServerCertificate=yes;')
        print("Conexión Correcta")
        return conexion
    except pyodbc.Error as e:
        print("Ha habido un problema al conectarse a la base de datos:", e)
        return None

# Hago una consulta a la base de datos para asegurar que funcione correctamente

def Consultas():
    conn = conexionDB()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        sql = "SELECT * FROM Datos"
        cur.execute(sql)
        filas = cur.fetchall()
        return filas
    except pyodbc.Error as e:
        print("Error ejecutando la consulta:", e)
        return []
    finally:
        cur.close()
        conn.close()

# Funcion para almacenar los datos en un dataframe y usarlos en Python

def cargar_datos():
    conn = conexionDB()
    if conn:
        query = "SELECT * from Datos"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    else:
        return pd.DataFrame([])

# Carga y visualización de los datos en la terminal

df = cargar_datos()
print(df.head())

# Boton para la actualización de los datos manualmente en la pagina de Streamlit
# Agregar este boton para actualizar los datos en la pagina #

if st.button('Actualizar datos'):
    df = cargar_datos()
    st.write(df.head())
#######################################################################################

import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

# Ignorar advertencias
warnings.filterwarnings('ignore')

# Definir titulo de la pagina en navegador, icono y expansion del contenido en la ventana

st.set_page_config(page_title="VIH Satistics", page_icon=":female-doctor: ",layout="wide")

# Titulo de la pagina en la interfaz con icono

st.title(" :female-doctor: VIH en la República Dominicana")

# Definicion de 2.5rem (40 pixeles) de espacio entre el borde superior de cada elemento y su contenido

st.markdown('<style>div.block-container{padding-top:2.5rem;}</style>',unsafe_allow_html=True)

# Crear seccion de filtros en un lado desplegable de la interfaz

st.sidebar.header("Filtros")

# Filtro de region

region = st.sidebar.multiselect(
    "Seleccionar región",
    df["Region"].unique()
)

if not region:
    df2 = df.copy() # Si no se selecciona region, usar todos los datos del df
else:
    df2 = df[df["Region"].isin(region)] # Si hay seleccion, usar los datos donde esta esa region

# Filtro de provincia

provincia = st.sidebar.multiselect("Seleccionar provincia", df2["Provincia"].unique())
if not provincia:
    df3 = df2.copy()
else:
    df3 = df2[df2["Provincia"].isin(provincia)]

# Filtro de año

anio = st.sidebar.multiselect("Seleccionar año", df3["Año"].unique())

# Coordinar filtros de region, provincia y año

if not region and not provincia and not anio:
    filtered_df = df
elif not provincia and not anio:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not anio:
    filtered_df = df[df["Provincia"].isin(provincia)]
elif provincia and anio:
    filtered_df = df3[df["Provincia"].isin(provincia) & df3["Año"].isin(anio)]
elif region and anio:
    filtered_df = df3[df["Region"].isin(region) & df3["Año"].isin(anio)]
elif region and provincia:
    filtered_df = df3[df["Region"].isin(region) & df3["Provincia"].isin(provincia)]
elif anio:
    filtered_df = df3[df3["Año"].isin(anio)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["Provincia"].isin(provincia) & df3["Año"].isin(anio)]

# Los casos se suman y se agrupan por provincia
category_df = df3.groupby(by = ["Provincia"], as_index = False)["Cant_Casos"].sum()

# Definicion de dos columnas en la interfaz
col1, col2 = st.columns((2))

# Grafica de barras

st.subheader("Casos por provincia")
fig = px.bar(category_df, x = "Provincia", y = "Cant_Casos", text = ['{:,.2f}'.format(int(x.replace(",", ""))) for x in category_df["Cant_Casos"]],
            template = "seaborn")
st.plotly_chart(fig,use_container_width=True, height = 200)
