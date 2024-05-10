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

 