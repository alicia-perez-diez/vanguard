#importamos las librerías
import pandas as pd
from funciones import leer_datos, limpiar_dataframes, crear_dataframe_principales_clientes, grafico_edad_clientes_principales, grafico_genero_clientes_principales,\
    grafico_fidelidad_clientes_principales, graficos_contacto_clientes_ultimos_meses, grafico_num_cuentas_clientes_principales, mapa_calor_valores_numericos,\
    grafico_dinero_y_num_cuentas, grafico_dinero_segun_edad, grafico_edad_genero_y_num_cuentas, grafico_edad_genero_y_dinero, grafico_proporcion_test_control,\
    grafico_drop_off_test_control, grafico_tiempo_promedio_entre_pasos_test_control, grafico_tasa_de_conversion_por_paso_test_control, grafico_tasa_conversion_test_control,\
    grafico_tasa_abandono_test_control, grafico_tiempo_permanencia_test_control, grafico_tiempo_permanencia_menor_10_secs

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

#mostramos el gráfico de barras con la cantidad de años que llevan los clientes principales siéndolo
grafico_fidelidad_clientes_principales(df_clientes_principales)

#mostramos dos gráficos de barras que muestran el número de contactos que han tenido los contactos principales en los últimos 6 meses
graficos_contacto_clientes_ultimos_meses(df_clientes_principales)

#mostramos el gráfico de tipo violín con la distribución del número de cuentas de los principales clientes
grafico_num_cuentas_clientes_principales(df_clientes_principales)

#mostramos el mapa de calor para ver la relación entre las distintas variables numéricas
mapa_calor_valores_numericos(df_clientes_principales)

#mostramos el gráfico de caja que muestra la relación entre el dinero en cuenta y número de cuentas de los clientes principales
grafico_dinero_y_num_cuentas(df_clientes_principales)

#mostramos el gráfico de barras para observar el dinero en cuenta según la edad de los principales clientes
grafico_dinero_segun_edad(df_clientes_principales)

#mostramos el gráfico de dispersión para observar la relación entre la edad, el género y el número de cuentas de los clientes principales
grafico_edad_genero_y_num_cuentas(df_clientes_principales)

#mostramos el gráfico de dispersión para observar la relación entre la edad, el género y el dinero en cuenta de los clientes principales
grafico_edad_genero_y_dinero(df_clientes_principales)

#empezamos con el análisis del test A/B

#mostramos el gráfico circular con la proporción de usuarios que vieron cada variación
grafico_proporcion_test_control(df_exp)

#mostramos los gráficos de barras que muestran el drop-off en cada paso para cada una de las variaciones: control y test
grafico_drop_off_test_control(df_exp, df_final_web_data)

#mostramos el gráfico de barras para visualizar el tiempo promedio que tardan los usuarios en ir de un paso a otro según la variación
grafico_tiempo_promedio_entre_pasos_test_control(df_exp, df_final_web_data)

#mostramos el gráfico de barras para visualizar la tasa de conversión por paso para cada una de las variaciones: control y test
grafico_tasa_de_conversion_por_paso_test_control(df_exp, df_final_web_data)
#DA ERROR

#mostramos el gráfico de barras para visualizar la tasa de conversión por variación: control y test
grafico_tasa_conversion_test_control(df_exp, df_final_web_data)

#mostramos el gráfico de barras para comparar la tasa de abandono por variación: contro y test
grafico_tasa_abandono_test_control(df_exp, df_final_web_data)

#mostramos el gráfico de barras para comparar el tiempo de permanencia por variación: control y test
grafico_tiempo_permanencia_test_control(df_exp, df_final_web_data)

#mostramos el gráfico de barras para ver cuántos usuarios permanecieron menos de 10 segundos en la página por variación: control y test
grafico_tiempo_permanencia_menor_10_secs(df_exp, df_final_web_data)
#DA ERROR

