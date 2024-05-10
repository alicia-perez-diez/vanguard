#importamos las librerías
import pandas as pd
from funciones import leer_datos

#llamamos al archivo desde el archivo yalm e importamos los dataframes
yalm_path = "../config.yaml"

df_final_demo, df_final_web_data, df_exp = leer_datos(yalm_path) 
