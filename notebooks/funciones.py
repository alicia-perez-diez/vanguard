def leer_datos(yalm_path):

    import pandas as pd
    import yaml

    #leemos el archivo Yaml en Python
    try:
        with open(yalm_path, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print('Error leyendo el archivo .yaml:', e)
        return None

    #importamos los dataframes
    try:
        df_final_demo = pd.read_csv(config['data']['demo_final'], sep=",", header=0, low_memory=False)
        pt_1 = pd.read_csv(config['data']['pt_1'], sep=",", header=0, low_memory=False)
        pt_2 = pd.read_csv(config['data']['pt_2'], sep=",", header=0, low_memory=False)
        #concatenamos los dataframes pt_1 y pt_2
        df_final_web_data = pd.concat([pt_1, pt_2], axis=0).reset_index(drop=True)
        df_exp = pd.read_csv(config['data']['exp_client'], sep=",", header=0, low_memory=False)
        return df_final_demo, df_final_web_data, df_exp
    except Exception as e:
        print('Error importando la data', e)
        return None

def limpiar_dataframes(df_final_demo, df_final_web_data, df_exp):

    import pandas as pd

    #eliminamos la columna clnt_tenure_mnth
    df_final_demo.drop("clnt_tenure_mnth", axis = 1, inplace = True)

    #Cambiamos el nombre de las columnas para que sean más descriptivos
    df_final_demo.columns = ["client_id","permanence_year","age","gender","num_accounts","total_balance","calls_months","login_month"]

    #eliminamos los valores duplicados de df_final_web_data
    df_final_web_data.drop_duplicates(keep='first', inplace=True)

    #cambiamos el formato de la columna 'date_time' a datetime.
    df_final_web_data["date_time"] = pd.to_datetime(df_final_web_data["date_time"], format='%Y-%m-%d %H:%M:%S')

    #cambiamos el nombre de la columna Variation a variation
    df_exp = df_exp.rename(columns={'Variation': 'variation'}, inplace=True)

    return df_final_demo, df_final_web_data, df_exp

def crear_dataframe_principales_clientes(df_final_demo):

    import pandas as pd

    #calcular los principales clientes basados en el dinero total de sus cuentas
    clientes_principales = df_final_demo.groupby('client_id')['total_balance'].sum().nlargest(50)

    #filtramos el dataframe original solo para los clientes principales
    df_clientes_principales = df_final_demo[df_final_demo['client_id'].isin(clientes_principales.index)]

    return df_clientes_principales

def grafico_edad_clientes_principales(df_clientes_principales):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    #agrupamos las edades por grupos de edad: jóvenes hasta 36, adultos jóvenes hasta 54 y adultos mayores a partir de 54.
    bins = [18, 36, 54, df_clientes_principales['age'].max()]
    labels = ['jóvenes', 'adultos jóvenes', 'adultos mayores']

    #añadimos la columna 'age_grouped' con las edades agrupadas al dataframe de clientes principales
    df_clientes_principales['age_grouped'] = pd.cut(df_clientes_principales['age'], bins=bins, labels=labels, include_lowest=True)

    #Histograma de edades de los principales clientes
    plt.figure(figsize=(10, 6))
    sns.histplot(df_clientes_principales['age_grouped'], bins=20, kde=True, color='skyblue')
    plt.title('Distribución de Edades de los Principales Clientes')
    plt.xlabel('Grupo de edad')
    plt.ylabel('Número de clientes')
    plt.show()

def grafico_genero_clientes_principales(df_clientes_principales):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #calculamos la frecuencia de género entre los clientes principales
    frecuencia_genero = df_clientes_principales['gender'].value_counts()

    #creamos gráfico circular para mostrar la proporción de géneros entre los principales clientes
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)  # 1 fila, 2 columnas, primer subgráfico
    plt.pie(frecuencia_genero, labels=frecuencia_genero.index, autopct='%1.1f%%', colors=sns.color_palette('Set3'))
    plt.title('Distribución de Género entre los Principales Clientes')
    plt.show()
    