# app.py

import streamlit as st
from funciones import leer_datos, limpiar_dataframes, grafico_proporcion_test_control

def main():
    st.set_option('deprecation.showPyplotGlobalUse', False)
    #reading data
    import pandas as pd
    from funciones import leer_datos, limpiar_dataframes, crear_dataframe_principales_clientes, crear_dataframe_promedio_tiempo_por_paso, guardar_como_csv,\
    grafico_edad_clientes_principales, grafico_genero_clientes_principales, grafico_fidelidad_clientes_principales, graficos_contacto_clientes_ultimos_meses,\
    grafico_num_cuentas_clientes_principales, mapa_calor_valores_numericos, grafico_dinero_y_num_cuentas, grafico_dinero_segun_edad, grafico_edad_genero_y_num_cuentas,\
    grafico_edad_genero_y_dinero, grafico_proporcion_test_control, grafico_drop_off_test_control, grafico_tiempo_promedio_entre_pasos_test_control,\
    grafico_tasa_de_conversion_por_paso_test_control, grafico_tasa_conversion_test_control,grafico_tasa_abandono_test_control, grafico_tiempo_permanencia_test_control,\
    grafico_tiempo_permanencia_menor_10_secs

    #llamamos al archivo desde el archivo yalm e importamos los dataframes
    yalm_path = "./config.yaml"

    df_final_demo, df_final_web_data, df_exp = leer_datos(yalm_path) 

    #llamamos a la función limpiar_dataframes
    df_final_demo, df_final_web_data, df_exp = limpiar_dataframes(df_final_demo, df_final_web_data, df_exp)

    #filtramos el dataframe df_final_demo para obtener a los 50 clientes con más dinero en la cuenta
    df_clientes_principales = crear_dataframe_principales_clientes(df_final_demo)

    #creamos un dataframe para calcular el tiempo promedio que tardan los usuarios en pasar de un paso a otro por variación: control y test
    df_transacciones_para_grafico = crear_dataframe_promedio_tiempo_por_paso(df_exp, df_final_web_data)
    
    """---------------------------------------------------------------------------------------------------"""
    st.title('Vanguard Dashboard')

    # Cargar la data
    data = leer_datos(yalm_path)
    
    # Interactive widgets
    st.sidebar.header('Controls')
    #Multiselect box for selecting variation to include in the analysis
    variation = st.sidebar.radio("Variation", ('All', 'Control', 'Test'))
    #Radio buttons for selecting gender to filter the data
    gender = st.sidebar.radio("Gender", ('All','U', 'M', 'F'))
    #Multiselect box for selecting steps 
    steps = st.sidebar.multiselect('Select Options',df_transacciones_para_grafico.steps.unique())
    print(steps)
    # Filters    
    filtered_data = df_transacciones_para_grafico
    if variation != 'All':
        filtered_data = filtered_data[filtered_data['variation'] == variation]
    if steps:
        filtered_data = filtered_data[filtered_data['steps'].isin(steps)]

    filtered_data_2 = df_final_demo if gender == 'All' else df_final_demo[df_final_demo['gender'] == gender]

    
    
    # Summary statistics
    #updated_summary = get_summary(filtered_data)
    #st.write("### Summary Statistics")
    #st.table(updated_summary) 

    # Display Users Data
    st.write("### Usuarios Data")
    st.dataframe(filtered_data_2)

    # Display Web Data
    #st.write("### Web Data")
    #st.dataframe(filtered_data_2)

    # Display Registro de Variacion
    st.write("### Registro de Variación")
    st.dataframe(filtered_data)


    #Histograma de edad de los clientes principales
    st.write("### Edad de los Clientes Principales")
    plt= grafico_edad_clientes_principales(df_clientes_principales)
    st.pyplot(plt)

    #Grafico circular por proporcion de genero 
    st.write("### Proporción de Género entre los Clientes Principales")
    plt= grafico_genero_clientes_principales(df_clientes_principales)
    st.pyplot(plt)

    #Grafico de barras de tiempo de fidelidad
    st.write("### Tiempo de Fidelidad de los Clientes Principales")
    plt= grafico_fidelidad_clientes_principales(df_clientes_principales)
    st.pyplot(plt)
    
    #Distribucion de numero de cuentas 
    st.write("### Distribución de Número de Cuentas de los Clientes Principales")
    plt= grafico_num_cuentas_clientes_principales(df_clientes_principales)
    st.pyplot(plt)
    
    #Grafico de caja de la relacion entre el dinero en cuenta y el numero de cuentas de los principales clientes
    st.write("### Relación entre Dinero en cuenta y Número de cuentas de los Clientes Principales")
    plt= grafico_dinero_y_num_cuentas(df_clientes_principales)
    st.pyplot(plt)

    #Grafico de dispersion entre la edad, genero y numeros de cuentas de los principales clientes
    st.write("### Relación entre Edad, Género y Número de cuentas de los Clientes Principales")
    plt= grafico_edad_genero_y_num_cuentas(df_clientes_principales)
    st.pyplot(plt)
    

    # Grafico proporción de usuarios
    st.write("### Proporción de Usuarios que vieron cada Variación")
    plt= grafico_proporcion_test_control(df_exp)
    st.pyplot(plt)

    # Grafico Dropp-off
    st.write("### Drop-off en cada paso por cada Variación")
    plt= grafico_drop_off_test_control(df_exp, df_final_web_data)
    st.pyplot(plt)

    #Grafico tiempo promedio entre pasos
    st.write("### tiempo promedio que tardan los usuarios en ir de un paso a otro según la variación")
    plt= grafico_tiempo_promedio_entre_pasos_test_control(df_exp, df_final_web_data)
    #st.pyplot(plt)
    st.plotly_chart(plt, use_container_width=True)

    #Grafico de conversion
    st.write("### Tasa de Conversión por Paso")
    plt= grafico_tasa_de_conversion_por_paso_test_control(df_exp, df_final_web_data)
    st.pyplot(plt)

    #Grafico de tasa de abandono
    st.write("### Tasa de Abandono por Conversión")
    plt= grafico_tasa_abandono_test_control(df_exp, df_final_web_data)
    st.pyplot(plt)

    #Grafico tiempo de permanencia 
    st.write("### Tiempo de Permanencia por Variación")
    plt= grafico_tiempo_permanencia_test_control(df_exp, df_final_web_data)
    st.pyplot(plt)

    
    


if __name__ == '__main__':
    main()