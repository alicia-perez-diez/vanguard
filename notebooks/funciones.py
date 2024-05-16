def leer_datos(yalm_path):

    """
    Lee los datos de archivos CSV especificados en el archivo YAML.

    Argumentos:
    - yalm_path (str): Ruta del archivo YAML que contiene la información de los archivos CSV.

    Devuelve:
    - df_final_demo (DataFrame de Pandas): DataFrame que contiene los datos finales de demostración.
    - df_final_web_data (DataFrame de Pandas): DataFrame que contiene los datos web finales.
    - df_exp (DataFrame de Pandas): DataFrame que contiene los datos de experimentos de clientes.

    Si hay algún error durante la lectura o importación de los datos, la función imprime un mensaje de error y retorna None.
    """

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

    """
    Realiza operaciones de limpieza en DataFrames específicos.

    Argumentos:
    - df_final_demo (DataFrame de Pandas): DataFrame que contiene los datos finales de demostración.
    - df_final_web_data (DataFrame de Pandas): DataFrame que contiene los datos web finales.
    - df_exp (DataFrame de Pandas): DataFrame que contiene los datos de experimentos de clientes.

    Devuelve:
    - df_final_demo (DataFrame de Pandas): DataFrame modificado de los datos finales de demostración.
    - df_final_web_data (DataFrame de Pandas): DataFrame modificado de los datos web finales.
    - df_exp (DataFrame de Pandas): DataFrame modificado de los datos de experimentos de clientes.

    Realiza varias operaciones de limpieza en los DataFrames proporcionados:
    """

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
    df_exp = df_exp.rename(columns={'Variation': 'variation'})

    #eliminamos datos nulos
    df_exp = df_exp.dropna()

    return df_final_demo, df_final_web_data, df_exp

def crear_dataframe_principales_clientes(df_final_demo):

    """
    Crea un nuevo DataFrame con los principales clientes basados en el dinero total de sus cuentas.

    Argumentos:
    - df_final_demo (DataFrame de Pandas): DataFrame que contiene los datos finales de demostración.

    Devuelve:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene únicamente los datos de los principales clientes.

    Esta función calcula los principales clientes basados en el dinero total de sus cuentas en el DataFrame proporcionado.
    Luego, filtra el DataFrame original solo para incluir los datos de los clientes principales y retorna este nuevo DataFrame.
    """

    import pandas as pd

    #calcular los principales clientes basados en el dinero total de sus cuentas
    clientes_principales = df_final_demo.groupby('client_id')['total_balance'].sum().nlargest(50)

    #filtramos el dataframe original solo para los clientes principales
    df_clientes_principales = df_final_demo[df_final_demo['client_id'].isin(clientes_principales.index)]

    return df_clientes_principales

def crear_dataframe_promedio_tiempo_por_paso(df_exp, df_final_web_data):

    """
    Crea un nuevo DataFrame para analizar el tiempo promedio por paso en el proceso de transacción.

    Argumentos:
    - df_exp (DataFrame de Pandas): DataFrame que contiene los datos de experimentos de clientes.
    - df_final_web_data (DataFrame de Pandas): DataFrame que contiene los datos web finales.

    Devuelve:
    - df_transacciones_para_grafico (DataFrame de Pandas): DataFrame que contiene los datos procesados para analizar el tiempo promedio por paso. 

    Esta función realiza las siguientes operaciones para crear el DataFrame de salida.
    Retorna el DataFrame procesado para su posterior análisis del tiempo promedio por paso en el proceso de transacción.
    """

    #eliminamos los datos nulos y con ellos se eliminan 20109 filas
    df_exp = df_exp.dropna(subset =["variation"])

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #ordenamos los valores del df por cliente id, visita id y
    df_transacciones = df_transacciones.sort_values(by=['client_id', 'visit_id', 'date_time'])

    #creamos una nueva columna en la que añadimos la fecha en la que el usuario realizó el paso anterior
    df_transacciones['time_last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['date_time'].shift(1)

    #creamos una nueva columna para añadir el paso anterior al actual
    df_transacciones['last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['process_step'].shift(1)

    #restamos la fecha del paso anterior a la del actual para ver cuánto ha tardado en pasar de un paso a otro
    df_transacciones['time_difference'] = df_transacciones['date_time'] - df_transacciones['time_last_step']

    #agregamos una nueva columna en la que incluimos el nombre del paso anterior y el paso actual
    df_transacciones['steps'] = df_transacciones['process_step'].astype(str) + '_' + df_transacciones['last_step'].astype(str)

    #transformamos el tiempo a segundos
    df_transacciones['difference_time_in_seconds'] = df_transacciones['time_difference'].dt.total_seconds()

    #eliminamos las filas que tienen valores nulos en time_difference, ya que son el primer paso realizado por el usuario en cada visita
    df_transacciones_para_grafico = df_transacciones.dropna(subset='difference_time_in_seconds')
   
    return df_transacciones_para_grafico

def guardar_como_csv(df, nombre_archivo):

    """
    Guarda un DataFrame como archivo CSV en una ubicación específica.

    Argumentos:
    - df (DataFrame de Pandas): DataFrame que se desea guardar como archivo CSV.
    - nombre_archivo (str): Nombre del archivo CSV.

    Esta función guarda el DataFrame proporcionado como un archivo CSV en una ubicación específica.
    La ruta de la carpeta donde se guarda el archivo CSV está predefinida en la variable 'ruta'.
    Utiliza os.path.join() para unir la ruta de la carpeta con el nombre del archivo proporcionado,
    generando así la ruta completa donde se guardará el archivo CSV.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente guarda el archivo CSV en la ubicación especificada.

    Ejemplo de uso:
    guardar_como_csv(df, "datos_guardados.csv")
    """

    import os

    #creamos una cadena que representa la ruta de la carpeta donde queremos guardar el archivo CSV.
    ruta = r'..\data\output'

    #utilizamos os.path.join() para unir esta ruta con el nombre del archivo proporcionado
    #generando así la ruta completa donde guardaremos el archivo csv.
    ruta_completa = os.path.join(ruta, nombre_archivo)
    df.to_csv(ruta_completa, sep=',', encoding='utf-8', index=False)

def grafico_edad_clientes_principales(df_clientes_principales):

    """
    Genera un gráfico de distribución de edades de los principales clientes.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico de distribución de edades de los principales clientes.
    """   

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

    """
    Genera un gráfico de distribución de géneros de los clientes principales.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """       
    
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

    """
    Genera un gráfico de distribución de los años que llevan los clientes principales siéndolo.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """    

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

    """
    Genera un gráfico de distribución del contacto con la empresa de los clientes principales en los últimos 6 meses.
    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """  
    
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

    """
    Genera un gráfico de distribución con el número de cuentas que tienen los clientes principales.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """  
    
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

    """
    Genera un mapa de calor entre todos los valores numéricos.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """  

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

    """
    Genera un gráfico de distribución del número de cuentas y dinero en cuenta de los clientes principales.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """  

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

    """
    Genera un gráfico de distribución del dinero en cuenta según la edad de los clientes principales.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """ 
    
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

    """
    Genera un gráfico que muestra la relación entre la edad, el género y el número de cuentas de los clientes principales.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """ 
    
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

    """
    Genera un gráfico que muestra la relación entre la edad, el género y el dinero en cuenta de los clientes principales.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """ 
    
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

    """
    Genera un gráfico de distribución entre los clientes principales que han visto la plataforma original y los que han visto el test.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """ 

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

    """
    Genera un gráfico que muestra la caída de usuarios entre los distintos pasos para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """ 

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

def grafico_tiempo_promedio_entre_pasos_test_control(df_exp, df_final_web_data):

    """
    Genera un gráfico que muestra el tiempo promedio entre pasos para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """

    import pandas as pd
    import plotly.express as px

    #eliminamos los datos nulos y con ellos se eliminan 20109 filas
    df_exp = df_exp.dropna(subset =["variation"])

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #ordenamos los valores del df por cliente id, visita id y
    df_transacciones = df_transacciones.sort_values(by=['client_id', 'visit_id', 'date_time'])

    #creamos una nueva columna en la que añadimos la fecha en la que el usuario realizó el paso anterior
    df_transacciones['time_last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['date_time'].shift(1)

    #creamos una nueva columna para añadir el paso anterior al actual
    df_transacciones['last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['process_step'].shift(1)

    #restamos la fecha del paso anterior a la del actual para ver cuánto ha tardado en pasar de un paso a otro
    df_transacciones['time_difference'] = df_transacciones['date_time'] - df_transacciones['time_last_step']

    #agregamos una nueva columna en la que incluimos el nombre del paso anterior y el paso actual
    df_transacciones['steps'] = df_transacciones['process_step'].astype(str) + '_' + df_transacciones['last_step'].astype(str)

    #eliminamos las filas que tienen valores nulos en time_difference, ya que son el primer paso realizado por el usuario en cada visita
    df_transacciones_para_grafico = df_transacciones.dropna(subset='time_difference')

    #creamos un nuevo df para el gráfico en el que agrupamos los pasos, la variación (si ha realizado el test o no) y el tiempo que han tardado los usuarios en ir de un paso a otro
    df_transacciones_por_tiempo = df_transacciones_para_grafico.groupby(by=['steps', 'variation'])['time_difference'].mean().reset_index()

    #realizamos un gráfico de barras agrupadas para comprobar de manera visual cuánto tiempo tardan los usuarios en ir de un paso a otro

    #ordenamos los pasos según el orden natural
    orden = ['start_start', 'start_step_1', 'start_step_2', 'start_step_3', 'start_confirm', 'step_1_start', 'step_1_step_1', 'step_1_step_2', 'step_1_step_3', 'step_1_confirm',\
        'step_2_start', 'step_2_step_1', 'step_2_step_2', 'step_2_step_3', 'step_2_confirm', 'step_3_start', 'step_3_step_1', 'step_3_step_2', 'step_3_step_3', 'step_3_confirm',\
        'confirm_start', 'confirm_step_1', 'confirm_step_2', 'confirm_step_3', 'confirm_confirm']

    #creamos el gráfico
    fig = px.bar(df_transacciones_por_tiempo, x="steps", y="time_difference", color="variation", barmode='group')

    #lo ordenamos según el listado de orden creado previamente
    fig.update_layout(xaxis=dict(categoryorder='array', categoryarray=orden))

    #modificamos el título y etiquetas del gráfico
    fig.update_layout(title="Tiempo promedio que tardan los usuarios en ir de un paso a otro según variación", xaxis_title='pasos', yaxis_title='tiempo promedio')

    #mostramos el gráfico
    fig.show()

def grafico_tasa_de_conversion_por_paso_test_control(df_exp, df_final_web_data):

    """
    Genera un gráfico que muestra la tasa de conversión por paso para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    #eliminamos los datos nulos y con ellos se eliminan 20109 filas
    df_exp = df_exp.dropna(subset =["variation"])

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #ordenamos los valores del df por cliente id, visita id y
    df_transacciones = df_transacciones.sort_values(by=['client_id', 'visit_id', 'date_time'])

    #creamos una nueva columna en la que añadimos la fecha en la que el usuario realizó el paso anterior
    df_transacciones['time_last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['date_time'].shift(1)

    #creamos una nueva columna para añadir el paso anterior al actual
    df_transacciones['last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['process_step'].shift(1)

    #restamos la fecha del paso anterior a la del actual para ver cuánto ha tardado en pasar de un paso a otro
    df_transacciones['time_difference'] = df_transacciones['date_time'] - df_transacciones['time_last_step']

    #agregamos una nueva columna en la que incluimos el nombre del paso anterior y el paso actual
    df_transacciones['steps'] = df_transacciones['process_step'].astype(str) + '_' + df_transacciones['last_step'].astype(str)

    #indicamos el orden en el que queremos que se realice el loop
    orden = ["start", "step_1", "step_2", "step_3", "confirm"]

    #creamos una nueva variable para cada tipo de variación
    variation = ['Test', 'Control']

    #creamos un nuevo dataframe
    df_stats = pd.DataFrame(columns=orden, index=variation)

    #recorremos cada variación
    for variation_i in variation:
        #inicializamos el orden en 0
        i=0
        #recorremos cada paso
        for step_i in orden[-4:]:
            #para cada variación
            df_temp = df_transacciones[df_transacciones['variation'] == variation_i]
            #calculamos la tasa de conversión de cada paso, es decir, de usuarios que pasan al siguiente paso desde el inmediatamente previo
            df_stats.loc[variation_i, orden[i]] = (df_temp[df_temp['steps'] == orden[i] + '_' + step_i]['visit_id'].count() / df_temp.groupby(by = 'process_step')['visit_id'].count()[orden[i]]) * 100
            #terminamos el loop
            i = i + 1
    
    #eliminamos la columna de confirm que tiene valores nulos
    df_stats.dropna(axis=1, inplace=True)

    #creamos el gráfico de la tasa de conversión para cada paso
    #definimos una paleta de colores suave
    sns.set_palette("pastel")

    #creamos el gráfico
    ax = df_stats.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Tasa de Conversión por Paso')
    plt.xlabel('Paso del Proceso')
    plt.ylabel('Tasa de Conversión')
    plt.xticks(rotation=45)
    plt.legend(title='variation')

    #agregamos etiquetas de texto para mostrar las tasas de conversión exactas en cada barra
    for p in ax.patches:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy() 
        ax.annotate(f'{height:.2f}', (x + width/2, y + height/2), ha='center', va='center')

    plt.tight_layout()
    
    #mostramos el gráfico
    plt.show()

def grafico_tasa_conversion_test_control(df_exp, df_final_web_data):

    """
    Genera un gráfico que muestra la tasa de conversión total para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """
    
    import pandas as pd
    import matplotlib.pyplot as plt

    #unimos los dataframes en uno solo utilizando la columna 'client_id' como clave
    df_merged_para_tasa_de_conversion_total = pd.merge(df_final_web_data, df_exp, on='client_id')

    #calculamos el número total de usuarios que completaron el proceso (llegaron al paso 'confirm')
    confirm_total_por_variacion = df_merged_para_tasa_de_conversion_total[df_merged_para_tasa_de_conversion_total['process_step'] == 'confirm'].groupby('variation')['client_id'].nunique()

    #calculamos el número total de usuarios que comenzaron el proceso (iniciaron el paso 'start')
    start_total_por_variacion = df_merged_para_tasa_de_conversion_total[df_merged_para_tasa_de_conversion_total['process_step'] == 'start'].groupby('variation')['client_id'].nunique()

    #calculamos la tasa de conversión total por variación
    conversion_rate_total = confirm_total_por_variacion / start_total_por_variacion

    #creamos el gráfico de barras
    plt.figure(figsize=(10, 6))
    conversion_rate_total.plot(kind='bar', color=['skyblue', 'pink'])

    #configuramos el título y etiquetas
    plt.title('Tasa de Conversión por Variación')
    plt.xlabel('Variación')
    plt.ylabel('Tasa de Conversión')
    plt.xticks(rotation=45)

    #mostramos el gráfico
    plt.tight_layout()
    plt.show()

def test_hipotesis_tasa_conversion(df_final_web_data, df_exp, alpha=0.05, alternative='greater'):

    """
    Función para realizar un test de hipótesis sobre la tasa de conversión entre cada una de las variaciones.
    
    Args:
        dataframes: df_final_web_data, df_exp.
        alpha (float, optional): Nivel de significancia. Por defecto es 0.05.
        alternative (str, optional): Dirección de la hipótesis alternativa. Puede ser 'greater' (mayor), 'less' (menor) o 'two-sided' (dos colas). Por defecto es 'greater'.
        
    Returns:
        str: Resultado del test de hipótesis.
    """

    import pandas as pd
    import scipy.stats as st
    
    #Unimos los dataframes en uno solo utilizando la columna 'client_id' como clave
    df_merged_para_tasa_de_conversion_total = pd.merge(df_final_web_data, df_exp, on='client_id')

    #calculamos el número total de usuarios que completaron el proceso (llegaron al paso 'confirm')
    confirm_total_por_variacion = df_merged_para_tasa_de_conversion_total[df_merged_para_tasa_de_conversion_total['process_step'] == 'confirm'].groupby('variation')['client_id'].nunique()

    #calculamos el número total de usuarios que comenzaron el proceso (iniciaron el paso 'start')
    start_total_por_variacion = df_merged_para_tasa_de_conversion_total[df_merged_para_tasa_de_conversion_total['process_step'] == 'start'].groupby('variation')['client_id'].nunique()

    #calculamos el ratio de conversion total por variación
    conversion_rate_total = confirm_total_por_variacion / start_total_por_variacion

    #filtramos entre los usuarios que han llegado al paso de confirm y creamos una columna que guarde el resultado
    df_confirm_visit_id = df_merged_para_tasa_de_conversion_total[df_merged_para_tasa_de_conversion_total['process_step'] == 'confirm'].groupby('visit_id')['client_id'].nunique().reset_index().rename(columns={'client_id' : 'confirm_binary'})

    #creamos otro dataframe con el visit_id y la variación realizada
    df_visit_id = df_merged_para_tasa_de_conversion_total[df_merged_para_tasa_de_conversion_total['process_step'] == 'start'][['visit_id', 'variation']]

    #unimos ambos dataframes
    df_conversion = df_visit_id.merge(df_confirm_visit_id, how='left', on='visit_id')

    #creamos los dos dataframes finales para el test de la hipótesis
    df_conversion_test = df_conversion[df_conversion['variation'] == 'Test'].fillna(0)
    df_conversion_control = df_conversion[df_conversion['variation'] == 'Control'].fillna(0)

    #calculamos el p_value
    t_stat, p_value = st.ttest_ind(df_conversion_test['confirm_binary'], df_conversion_control['confirm_binary'], equal_var=False, alternative="greater")    
    
    #imprimimos el resultado según la dirección de la hipótesis alternativa
    if alternative == "greater":
        if p_value > alpha:
            print("No hemos sido capaces de rechazar la hipótesis nula.")
        else:
            print("Rechazamos la hipótesis nula.")
    elif alternative == "less":
        if p_value > alpha:
            print("No hemos sido capaces de rechazar la hipótesis nula.")
        else:
            print("Rechazamos la hipótesis nula.")
    elif alternative == "two-sided":
        if p_value > alpha:
            print("No hemos sido capaces de rechazar la hipótesis nula.")
        else:
            print("Rechazamos la hipótesis nula.")
    else:
        print("Dirección de hipótesis no válida. Por favor, elige 'greater', 'less' o 'two-sided'.")

def grafico_tasa_abandono_test_control(df_exp, df_final_web_data):

    """
    Genera un gráfico que muestra la tasa de abandono para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    df_merged_para_tasa_de_abandono = pd.merge(df_final_web_data, df_exp, on='client_id')

    #calculamos el número de usuarios que comenzaron el proceso para cada variación
    variacion_total = df_merged_para_tasa_de_abandono.groupby('variation')['client_id'].nunique()

    #calculamos el número de usuarios que completaron el proceso para cada variación
    proceso_completado = df_merged_para_tasa_de_abandono[df_merged_para_tasa_de_abandono['process_step'] == 'confirm'].groupby('variation')['client_id'].nunique()

    #calculamos la tasa de abandono total para cada variación
    ratio_de_abandono = 1 - (proceso_completado / variacion_total)

    #graficamos la tasa de abandono total por variación
    #ajustamos el tamaño
    plt.figure(figsize=(8, 6))

    #creamos el gráfico
    sns.barplot(x=ratio_de_abandono.index, y=ratio_de_abandono.values, palette='PiYG')
    
    #otorgamos título y etiquetas
    plt.title('Tasa de Abandono Total por Variación')
    plt.xlabel('Variation')
    plt.ylabel('Tasa de Abandono')
    
    #ajustamos configuración y mostramos el gráfico
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def grafico_tiempo_permanencia_test_control(df_exp, df_final_web_data):

    """
    Genera un gráfico que muestra el tiempo de permanencia de los usuarios para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
     #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #agrupamos el dataframe por variación y tiempo entrada y de salida de cada usuario por id de visita
    df_tiempo_de_permanencia = df_transacciones.groupby(by=['variation', 'visit_id'])['date_time'].agg(['max', 'min']).reset_index()

    #agregamos una columna con el tiempo total por sesión de cada id de visita
    df_tiempo_de_permanencia['difference_time'] = df_tiempo_de_permanencia['max'] - df_tiempo_de_permanencia['min']

    #transformamos el tiempo a segundos
    df_tiempo_de_permanencia['difference_time_in_seconds'] = df_tiempo_de_permanencia['difference_time'].dt.total_seconds()

    #calculamos la media de tiempo de permanencia total por cada variación
    df_tiempo_de_permanencia_total = df_tiempo_de_permanencia.groupby('variation')['difference_time_in_seconds'].agg('mean')

    #graficamos el tiempo medio de permanencia en el sitio web por variación
    #ajustamos el tamaño
    df_tiempo_de_permanencia_total.plot(kind='bar', figsize=(8, 6))
    
    #creamos el gráfico
    sns.barplot(x=df_tiempo_de_permanencia_total.index, y=df_tiempo_de_permanencia_total.values, palette='pastel')
    
    #otorgamos el título y las etiquetas
    plt.title('Tiempo Medio de Permanencia en la plataforma')
    plt.xlabel('Variation')
    plt.ylabel('Tiempo Medio de Permanencia (segundos)')

    #ajustamos configuración y mostramos el gráfico
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def test_hipotesis_tiempo_permanencia(df_final_web_data, df_exp, alpha=0.05, alternative='greater'):

    """
    Función para realizar un test de hipótesis sobre la diferencia de tiempo promedio entre cada una de las variaciones.
    
    Args:
        dataframes: df_final_web_data, df_exp.
        alpha (float, optional): Nivel de significancia. Por defecto es 0.05.
        alternative (str, optional): Dirección de la hipótesis alternativa. Puede ser 'greater' (mayor), 'less' (menor) o 'two-sided' (dos colas). Por defecto es 'greater'.
        
    Returns:
        str: Resultado del test de hipótesis.
    """

    import pandas as pd
    import scipy.stats as st
    
    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #ordenamos los valores del df por cliente id, visita id y
    df_transacciones = df_transacciones.sort_values(by=['client_id', 'visit_id', 'date_time'])

    #creamos una nueva columna en la que añadimos la fecha en la que el usuario realizó el paso anterior
    df_transacciones['time_last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['date_time'].shift(1)

    #creamos una nueva columna para añadir el paso anterior al actual
    df_transacciones['last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['process_step'].shift(1)

    #restamos la fecha del paso anterior a la del actual para ver cuánto ha tardado en pasar de un paso a otro
    df_transacciones['time_difference'] = df_transacciones['date_time'] - df_transacciones['time_last_step']

    #agregamos una nueva columna en la que incluimos el nombre del paso anterior y el paso actual
    df_transacciones['steps'] = df_transacciones['process_step'].astype(str) + '_' + df_transacciones['last_step'].astype(str)

    #agrupamos el dataframe por variación y tiempo entrada y de salida de cada usuario por id de visita
    df_tiempo_de_permanencia = df_transacciones.groupby(by=['variation', 'visit_id'])['date_time'].agg(['max', 'min']).reset_index()

    #agregamos una columna con el tiempo total por sesión de cada id de visita
    df_tiempo_de_permanencia['difference_time'] = df_tiempo_de_permanencia['max'] - df_tiempo_de_permanencia['min']

    #transformamos el tiempo a segundos
    df_tiempo_de_permanencia['difference_time_in_seconds'] = df_tiempo_de_permanencia['difference_time'].dt.total_seconds()

    #creamos los dos dataframes finales para el análisis
    df_tiempo_de_permanencia_control = df_tiempo_de_permanencia[(df_tiempo_de_permanencia['variation'] == 'Control')]['difference_time_in_seconds']
    #creamos el segundo dataframe
    df_tiempo_de_permanencia_test = df_tiempo_de_permanencia[(df_tiempo_de_permanencia['variation'] == 'Test')]['difference_time_in_seconds']

    #calculamos el p_value
    t_stat, p_value = st.ttest_ind(df_tiempo_de_permanencia_test, df_tiempo_de_permanencia_control, equal_var=False, alternative=alternative)
    
    #mostramos si se rechaza o no la hipótesis nula según la alternativa elegida por el usuario y el valor de alpha
    if alternative == "greater":
        if p_value > alpha:
            return "No hemos sido capaces de rechazar la hipótesis nula."
        else:
            return "Rechazamos la hipótesis nula."
    elif alternative == "less":
        if p_value > alpha:
            return "No hemos sido capaces de rechazar la hipótesis nula."
        else:
            return "Rechazamos la hipótesis nula."
    elif alternative == "two-sided":
        if p_value > alpha:
            return "No hemos sido capaces de rechazar la hipótesis nula."
        else:
            return "Rechazamos la hipótesis nula."
    else:
        return "Dirección de hipótesis no válida. Por favor, elige 'greater', 'less' o 'two-sided'."


def grafico_tiempo_permanencia_menor_10_secs(df_exp, df_final_web_data):

    """
    Genera un gráfico que muestra la cantidad de usuarios que permanecieron menos de 10 segundos en la plataforma para las distintas variaciones de test y control.

    Argumentos:
    - df_clientes_principales (DataFrame de Pandas): DataFrame que contiene los datos de los principales clientes.

    Retorna:
    - None: Esta función no devuelve ningún valor, simplemente muestra el gráfico.
    """

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    #agrupamos el df_final_web_data con df_exp para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    #agrupamos el dataframe por variación y tiempo entrada y de salida de cada usuario por id de visita
    df_tiempo_de_permanencia = df_transacciones.groupby(by=['variation', 'visit_id'])['date_time'].agg(['max', 'min']).reset_index()

    #agregamos una columna con el tiempo total por sesión de cada id de visita
    df_tiempo_de_permanencia['difference_time'] = df_tiempo_de_permanencia['max'] - df_tiempo_de_permanencia['min']

    #transformamos el tiempo a segundos
    df_tiempo_de_permanencia['difference_time_in_seconds'] = df_tiempo_de_permanencia['difference_time'].dt.total_seconds()

    #calculamos cuántos usuarios han estado menos de 10 segundos en la página
    tiempo_permanencia_menor_10_secs = (df_tiempo_de_permanencia['difference_time_in_seconds'] <= 10).groupby(df_tiempo_de_permanencia['variation']).sum()

    #creamos el gráfico
    #ajustamos el tamaño
    plt.figure(figsize=(10, 6))
    tiempo_permanencia_menor_10_secs.plot(kind='bar')
    
    #creamos el gráfico
    sns.barplot(x=tiempo_permanencia_menor_10_secs.index, y=tiempo_permanencia_menor_10_secs.values, palette='Spectral')
    
    #otorgamos título, etiquetas y configuramos
    plt.title('Tiempo de Permanencia <= 10 Segundos')
    plt.xlabel('Variación')
    plt.ylabel('Número de Usuarios')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    #mostramos el gráfico
    plt.show()

def normalizar_distribucion_tiempo_permanencia(df_final_web_data, df_exp, version='Control'):
    
    """
    Función para normalizar la distribución del tiempo de permanencia.

    Args:
    df_final_web_data (DataFrame): dataframe principal para generar los dataframes finales.
    df_exp: dataframe principal para generar los dataframes finales.
    version = 'Control' o 'Test'.

    Return:
    DataFrame: El DataFrame con la columna normalizada y algunas estadísticas.
    """

    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    from scipy import stats
    from sklearn.preprocessing import PowerTransformer, StandardScaler
    from scipy.stats import johnsonsu, kstest

    # Agrupar el dataframe final con el experimento para añadir si el cliente ha visto la plataforma original o el test
    df_transacciones = df_final_web_data.merge(df_exp, how='left', left_on='client_id', right_on='client_id').dropna(subset='variation')

    # Ordenar los valores del dataframe por cliente id, visita id y fecha
    df_transacciones = df_transacciones.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Crear una nueva columna en la que añadimos la fecha en la que el usuario realizó el paso anterior
    df_transacciones['time_last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['date_time'].shift(1)

    # Crear una nueva columna para añadir el paso anterior al actual
    df_transacciones['last_step'] = df_transacciones.groupby(by=['client_id', 'visit_id'])['process_step'].shift(1)

    # Restar la fecha del paso anterior a la del actual para ver cuánto ha tardado en pasar de un paso a otro
    df_transacciones['time_difference'] = df_transacciones['date_time'] - df_transacciones['time_last_step']

    # Agregar una nueva columna en la que incluimos el nombre del paso anterior y el paso actual
    df_transacciones['steps'] = df_transacciones['process_step'].astype(str) + '_' + df_transacciones['last_step'].astype(str)

    # Agrupar el dataframe por variación y tiempo de entrada y salida de cada usuario por id de visita
    df_tiempo_de_permanencia = df_transacciones.groupby(by=['variation', 'visit_id'])['date_time'].agg(['max', 'min']).reset_index()

    # Agregar una columna con el tiempo total por sesión de cada id de visita
    df_tiempo_de_permanencia['difference_time'] = df_tiempo_de_permanencia['max'] - df_tiempo_de_permanencia['min']
    
    # Transformar el tiempo a segundos
    df_tiempo_de_permanencia['difference_time_in_seconds'] = df_tiempo_de_permanencia['difference_time'].dt.total_seconds()

    # Quedarse solo con la columna de variación y la diferencia de tiempo en segundos
    df_tiempo_de_permanencia = df_tiempo_de_permanencia[['variation', 'difference_time_in_seconds']]

    # Crear los dataframes finales para el análisis distinguiendo por variación: control y test
    df_tiempo_de_permanencia_control = df_tiempo_de_permanencia[df_tiempo_de_permanencia['variation'] == 'Control']
    df_tiempo_de_permanencia_test = df_tiempo_de_permanencia[df_tiempo_de_permanencia['variation'] == 'Test']
    """
    if version == 'Control':
        standardized_data = ((df_tiempo_de_permanencia_control['difference_time_in_seconds'] - df_tiempo_de_permanencia_control['difference_time_in_seconds'].mean()) /
                             df_tiempo_de_permanencia_control['difference_time_in_seconds'].std())
        ks_test_statistic, ks_p_value = stats.kstest(standardized_data, 'norm')
        if ks_p_value < 0.05:
            print('La distribución de tiempo de permanencia en la versión de Control es diferente a una distribución normal')
        else:
            print('La distribución de tiempo de permanencia en la versión de Control no es significativamente diferente a la normal')
    else:  # Para la versión de Test
        standardized_data = ((df_tiempo_de_permanencia_test['difference_time_in_seconds'] - df_tiempo_de_permanencia_test['difference_time_in_seconds'].mean()) /
                             df_tiempo_de_permanencia_test['difference_time_in_seconds'].std())
        ks_test_statistic, ks_p_value = stats.kstest(standardized_data, 'norm')
    """

    #eliminamos los outliers
    Q1 = df_tiempo_de_permanencia_control['difference_time_in_seconds'].quantile(0.25)
    Q3 = df_tiempo_de_permanencia_control['difference_time_in_seconds'].quantile(0.75)
    IQR = Q3 - Q1

    #establecemos los límites de los outliers
    limite_bajo = Q1 - 1 * IQR
    limite_alto = Q3 + 1 * IQR

    #identificamos los outliers y los filtramos de la tabla
    df_tiempo_de_permanencia_control = df_tiempo_de_permanencia_control[(df_tiempo_de_permanencia_control['difference_time_in_seconds'] >= limite_bajo) & (df_tiempo_de_permanencia_control['difference_time_in_seconds'] <= limite_alto)]


    # Realizar la transformación de Johnson-SU
    params = johnsonsu.fit(df_tiempo_de_permanencia_control['difference_time_in_seconds'])
    transformed_data = johnsonsu(*params).rvs(len(df_tiempo_de_permanencia_control['difference_time_in_seconds']))
    standardized_transformed_data = StandardScaler().fit_transform(transformed_data.reshape(-1, 1))

    # Realizar la prueba de Kolmogorov-Smirnov para normalidad en los datos transformados
    ks_result = kstest(standardized_transformed_data.flatten(), 'norm')

    # Graficar la distribución transformada
    sns.histplot(transformed_data, kde=False)
    plt.title("Distribución Johnson-SU")
    plt.show()

    import plotly.express as px
    px.data.tips()
    fig = px.histogram(pd.DataFrame(transformed_data)[0], nbins=100)
    fig.show()

    # Conclusión
    if ks_p_value < 0.05:
        print('La distribución no se ha podido normalizar.')
        print('Se emplearán algoritmos que permitan distribuciones no normales.')
    else:
        print('La distribución se ha normalizado con éxito.')