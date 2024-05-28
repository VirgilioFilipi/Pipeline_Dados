import AgricultureDB
from datetime import date
import configparser
import sys
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def main():

    # Lê as configurações do arquivo config.ini
    config = configparser.ConfigParser()
    config.read('../config.ini')

    if 'Agriculture' not in config:
        print("Seção 'Agriculture' não encontrada no arquivo config.ini")
        sys.exit(1)
    try:
        debug_mode = config.get('Agriculture', 'debug_mode')   
        start_year = config.get('Agriculture', 'start_year')  
        path_db = config.get('Agriculture', 'path_db') 


    except (configparser.NoOptionError, configparser.NoSectionError) as e:
        print(f"Erro ao ler configurações do arquivo config.ini: {e}")
        sys.exit(1)

    if debug_mode == "false":
        null = open(os.devnull, 'w')
        old_stdout = sys.stdout
        sys.stdout = null

    db = AgricultureDB.AgricultureDB(path_db)    

    current_year = date.today().year
    years = str(start_year) + '-' + str(current_year)

    print(years)

    db.insert_or_update(years)
    print("Dados inseridos/atualizados com sucesso: ", years)

    # db.delete(2020)

    if debug_mode == "true":

        conn = sqlite3.connect(path_db)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM VW_produtividade")
        rows = cursor.fetchall()

        conn.close()

        df = pd.DataFrame(rows, columns=['estado', 'ano', 'produtividade'])

        print("Valores nulos: ",df.isnull().values.any())
        print("Quantidade de valores nulos em produtividade: ", df['produtividade'].isnull().sum())

        # Optei por substituir valores nulos por zero na coluna 'produtividade' para evitar erro no sort_values da media
        df['produtividade'] = df['produtividade'].fillna(0)

        produtividade_media = df.groupby('estado', observed=True)['produtividade'].mean().sort_values(ascending=False)

        df['estado'] = pd.Categorical(df['estado'], categories=produtividade_media.index, ordered=True)
        df = df.sort_values('estado')

        anos = sorted(df['ano'].unique())

        fig, axs = plt.subplots(len(anos), 1, figsize=(10, 5 * len(anos)), sharex=True, 
                        gridspec_kw={'hspace': 0.5})  

        for i, ano in enumerate(anos):
            subset = df[df['ano'] == ano]
            x = np.arange(len(subset['estado'])) 
            axs[i].bar(x, subset['produtividade'], color='skyblue')
            axs[i].set_title(f'Produtividade por Estado em {ano}')
            axs[i].set_xlabel('Estado')
            axs[i].set_ylabel('Produtividade')
            axs[i].set_xticks(x)
            axs[i].set_xticklabels(subset['estado'])
            
            for j, estado in enumerate(subset['estado']):
                axs[i].text(j, 0.1, estado, rotation=90, ha='center')

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()