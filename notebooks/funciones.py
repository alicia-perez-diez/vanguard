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

    print('jóvenes hasta 36, adultos jóvenes hasta 54 y adultos mayores a partir de 54')

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

    print('M = Masculino, F = Femenino, U = NS/NC')

    
def grafico_fidelidad_clientes_principales(df_clientes_principales):

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    #agrupamos los años que llevan los clientes siéndolo hasta 5 clientes nuevos, hasta 15 clientes consolidados y a partir de ahí clientes antiguos
    bins = [0, 5, 15, df_clientes_principales['age'].max()]
    labels = ['Clientes nuevos', 'Clientes consolidados', 'Clientes antiguos']

    #añadimos una columna al dataframe df_clientes_principales llamada permanence_year_grouped para guardar esta nueva agrupación
    df_clientes_principales['permanence_year_grouped'] = pd.cut(df_clientes_principales['permanence_year'], bins=bins, labels=labels, include_lowest=True)

    #creamos un gráfico de barras para visualizar la distribución
    plt.figure(figsize=(10, 6))
    sns.countplot(x='permanence_year_grouped', data=df_clientes_principales, palette='pastel')
    plt.title('Distribución de la fidelidad de los clientes principales')
    plt.xlabel('Tiempo de permanencia')
    plt.ylabel('Número de años')
    plt.show()

    print('0-5 = clientes nuevos, 5-15 = clientes consolidados, >15 = clientes antiguos')

def graficos_contacto_clientes_ultimos_meses(df_clientes_principales):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #crear una figura con dos subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 5))

    #gráfico de barras de interacciones en la web en los últimos 6 meses de los principales clientes
    sns.countplot(x='login_month', data=df_clientes_principales, palette='coolwarm', ax=axes[0])
    axes[0].set_title('Interacciones en la plataforma de los clientes principales en los últimos 6 meses')
    axes[0].set_xlabel('Num de accesos a la plataforma')
    axes[0].set_ylabel('Num de usuarios')

    #gráfico de barras de clientes que hablaron en los últimos 6 meses de los principales clientes
    sns.countplot(x='calls_months', data=df_clientes_principales, palette='pastel', ax=axes[1])
    axes[1].set_title('Llamadas de los Principales Clientes en los últimos 6 meses')
    axes[1].set_xlabel('Num de llamadas')
    axes[1].set_ylabel('Num de usuarios')

    #ajustamos el espaciado entre los subplots
    plt.tight_layout()

    #mostramos el gráfico combinado
    plt.show()

def grafico_num_cuentas_clientes_principales(df_clientes_principales):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #ajustamos el tamaño
    plt.figure(figsize=(10, 8))

    #creamos el gráfico de violín
    sns.violinplot(x=df_clientes_principales['num_accounts'], inner='quartile', palette='pastel')
    
    #definimos título y etiquetas
    plt.title('Distribución del Número de Cuentas de los Principales Clientes')
    plt.xlabel('Número de Cuentas')
    plt.ylabel('Densidad')

    #mostramos el gráfico
    plt.show()

def mapa_calor_valores_numericos(df_clientes_principales):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #calculamos la matriz de correlación para crear un mapa de calor que muestre la relación entre variables numéricas
    matriz_de_correlacion = df_clientes_principales[['total_balance', 'age', 'num_accounts']].corr()

    #ajustamos el tamaño
    plt.figure(figsize=(8, 6))

    #creamos el mapa de calor
    sns.heatmap(matriz_de_correlacion, annot=True, cmap='coolwarm', fmt=".2f")

    #otorgamos un título
    plt.title('Matriz de Correlación')

    #mostramos el gráfico
    plt.show()

def grafico_dinero_y_num_cuentas(df_clientes_principales):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #ajustamos el tamaño del gráfico
    plt.figure(figsize=(10, 8))

    #creamos el gráfico de cajas
    sns.boxplot(x=df_clientes_principales['num_accounts'], y=df_clientes_principales['total_balance'], palette='coolwarm')
    
    #otorgamos título y etiquetas
    plt.title('Dinero en Cuenta de los Principales Clientes por Número de Cuentas')
    plt.xlabel('Número de Cuentas')
    plt.ylabel('Dinero en Cuenta')

    #mostramos el gráfico
    plt.show()

def grafico_dinero_segun_edad(df_clientes_principales):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #agrupamos las edades por grupos de edad: jóvenes hasta 36, adultos jóvenes hasta 54 y adultos mayores a partir de 54.
    bins = [18, 36, 54, df_clientes_principales['age'].max()]
    labels = ['jóvenes', 'adultos jóvenes', 'adultos mayores']

    #añadimos la columna 'age_grouped' con las edades agrupadas al dataframe de clientes principales
    df_clientes_principales['age_grouped'] = pd.cut(df_clientes_principales['age'], bins=bins, labels=labels, include_lowest=True)

    #ajustamos el tamaño del gráfico
    plt.figure(figsize=(10, 6))

    #creamos el gráfico de barras
    sns.barplot(x='age_grouped', y='num_accounts', data=df_clientes_principales, palette='pastel', errorbar=None)
    
    #otorgamos título y etiquetas
    plt.title('Distribución del dinero en cuenta por edad')
    plt.xlabel('Grupo de edad')
    plt.ylabel('Dinero en cuenta (media)')
    
    #mostramos el gráfico
    plt.show()

    print('jóvenes hasta 36, adultos jóvenes hasta 54 y adultos mayores a partir de 54')

def grafico_edad_genero_y_num_cuentas(df_clientes_principales):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    #ajustamos el tamaño del gráfico
    plt.figure(figsize=(10, 6))
    
    #creamos el gráfico
    sns.scatterplot(x='age', y='num_accounts', data=df_clientes_principales, hue='gender', palette='Set2')
    
    #asignamos título, etiquetas y leyenda
    plt.title('Relación entre Edad y Número de Cuentas Abiertas')
    plt.xlabel('Edad')
    plt.ylabel('Número de Cuentas Abiertas')
    plt.legend(title='Género', loc='upper left')

    #mostramos el gráfico
    plt.show()

def grafico_edad_genero_y_dinero(df_clientes_principales):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #ajustamos el tamaño
    plt.figure(figsize=(10, 6))

    #creamos el gráfico
    sns.scatterplot(x='age', y='total_balance', data=df_clientes_principales, hue='gender', palette='Set2')
    
    #asignamos título, etiquetas y legenda
    plt.title('Relación entre Edad, Género y Dinero en cuenta')
    plt.xlabel('Edad')
    plt.ylabel('Dinero en cuenta')
    plt.legend(title='Género', loc='upper left')

    #mostramos el gráfico
    plt.show()

def grafico_proporcion_test_control(df_exp):

    import pandas as pd
    import matplotlib.pyplot as plt

    #contamos el número de usuarios que han visto la página de control y la de test
    control_users = df_exp[df_exp['variation'] == 'Control']['client_id'].nunique()
    test_users = df_exp[df_exp['variation'] == 'Test']['client_id'].nunique()

    #creamos una lista con los nombres de las variantes y otra lista con los tamaños correspondientes
    variantes = ['Control', 'Test']
    tamaños = [control_users, test_users]

    #creamos el gráfico circular
    #ajustamos el tamaño
    plt.figure(figsize=(8, 6))

    #creamos el gráfico
    patches, texts, _ = plt.pie(tamaños, labels=variantes, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightgreen'])
     
    plt.title('Distribución de usuarios entre la página de control y la de test')
    plt.axis('equal')

    #añadimos el número exacto de usuarios
    for i, texto in enumerate(texts):
        texto.set_text(f"{variantes[i]}: {tamaños[i]} usuarios")

    plt.show()

def grafico_drop_off_test_control(df_exp, df_final_web_data):

    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd

    # creamos el dataframe solo con los usuarios que han realizado el test
    df_test = df_final_web_data.merge(df_exp[df_exp['variation'] == 'Test'], how='inner', on='client_id')

    #creamos el dataframe solo con los usuarios que han realizado la versión original
    df_control = df_final_web_data.merge(df_exp[df_exp['variation'] == 'Control'], how='inner', on='client_id')

    #ordenamos los pasos para que se muestren en el orden natural
    orden = ['start', 'step_1', 'step_2', 'step_3', 'confirm']

    #convertimos la columna process_step del test a tipo categórico con el orden deseado
    df_test['process_step'] = pd.Categorical(df_test['process_step'], categories=orden, ordered=True)

    #convertimos la columna process_step del control a tipo categórico con el orden deseado
    df_control['process_step'] = pd.Categorical(df_control['process_step'], categories=orden, ordered=True)

    #creamos los histogramas ordenados
    fig, axes = plt.subplots(1, 2, figsize=(12, 5)) 

    #graficamos el avance de los usuarios en la versión original de la plataforma
    sns.histplot(df_control['process_step'], bins=20, kde=True, color='green', ax=axes[0])
    axes[0].set_title('Drop off en la versión original de la plataforma', pad=30)  # Ajustamos la distancia entre el título y el gráfico
    axes[0].set_xlabel('Pasos')
    axes[0].set_ylabel('Número de usuarios')
    axes[0].set_ylim(0, 120000)

    #graficamos el avance de los usuarios que hicieron el test en la plataforma
    sns.histplot(df_test['process_step'], bins=20, kde=True, color='skyblue', ax=axes[1])
    axes[1].set_title('Drop off en la versión test de la plataforma', pad=30)  # Ajustamos la distancia entre el título y el gráfico
    axes[1].set_xlabel('Pasos')
    axes[1].set_ylabel('Número de usuarios')
    axes[1].set_ylim(0, 120000)

    plt.tight_layout()  # Ajustamos el diseño para evitar solapamientos

    #mostramos los gráficos
    plt.show()

