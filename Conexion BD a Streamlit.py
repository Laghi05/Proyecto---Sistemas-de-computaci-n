# Importacion del modulo de instalacion de paquetes
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

if st.button('Actualizar datos'):
    df = cargar_datos()
    st.write(df.head())
#######################################################################################