#importamos las librerías
import pandas as pd
from funciones import leer_datos, limpiar_dataframes, crear_dataframe_principales_clientes, grafico_edad_clientes_principales, grafico_genero_clientes_principales

#llamamos al archivo desde el archivo yalm e importamos los dataframes
yalm_path = "../config.yaml"

df_final_demo, df_final_web_data, df_exp = leer_datos(yalm_path) 

#llamamos a la función limpiar_dataframes
limpiar_dataframes(df_final_demo, df_final_web_data, df_exp)

#filtramos el dataframe df_final_demo para obtener a los 50 clientes con más dinero en la cuenta
df_clientes_principales = crear_dataframe_principales_clientes(df_final_demo)

#mostramos el histograma con la edad de los clientes principales
grafico_edad_clientes_principales(df_clientes_principales)

#mostramos el gráfico circular con la proporción de géneros entre los clientes principales
grafico_genero_clientes_principales(df_clientes_principales)



