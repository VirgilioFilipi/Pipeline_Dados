import sqlite3
import requests
import os

class AgricultureDB:
    """Classe para manipulação de dados relacionados à agricultura em um banco de dados SQLite."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        """Configura o banco de dados SQLite, criando tabelas e view."""

        if os.path.exists(self.db_name):
            conn = self.create_connection(self.db_name)

            if conn is not None:
                print("Banco de dados já existe. Excluindo dados existentes...")
                cur = conn.cursor()
                cur.execute("DELETE FROM area_colhida;")
                cur.execute("DELETE FROM quantidade_produzida;")
                conn.commit()
                self.create_view(conn)
                conn.close()
                print("Dados excluídos com sucesso!")
            else:
                print("Erro ao criar conexão com o banco de dados.")
        else:
            conn = self.create_connection(self.db_name)

            if conn is not None:
                print("Banco de dados não encontrado. Criando novo banco de dados...")
                self.create_harvested_table(conn)
                self.create_produced_table(conn)
                self.create_view(conn)
                conn.close()
                print("Banco de dados criado com sucesso!")
            else:
                print("Erro ao criar conexão com o banco de dados.")


    def create_connection(self, db_file):
        """
        Cria uma conexão com o banco de dados SQLite.

        Parameters:
            db_file (str): Nome do arquivo de banco de dados SQLite.

        Returns:
            conn: Objeto de conexão SQLite.
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except sqlite3.Error as e:
            print(e)
        return None
    
    def create_harvested_table(self, conn):
        """
        Cria a tabela de área colhida no banco de dados SQLite.

        Parameters:
            conn: Objeto de conexão SQLite.
        """
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS area_colhida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            municipio TEXT NOT NULL,
            codigo INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            colhida INTEGER
        )
        ''')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_area_colhida_municipio ON area_colhida(municipio)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_area_colhida_ano ON area_colhida(ano)')
        conn.commit()

    def create_produced_table(self, conn):
        """
        Cria a tabela de quantidade produzida no banco de dados SQLite.

        Parameters:
            conn: Objeto de conexão SQLite.
        """
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS quantidade_produzida (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            municipio TEXT NOT NULL,
            codigo INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            produzida INTEGER
        )
        ''')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_produzida_municipio ON quantidade_produzida(municipio)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_produzida_ano ON quantidade_produzida(ano)')
        conn.commit()

   
    def create_view(self, conn):
        """
        Cria a visualização de produtividade no banco de dados SQLite.

        Parameters:
            conn: Objeto de conexão SQLite.
        """
        cur = conn.cursor()
        cur.execute('''
        CREATE VIEW IF NOT EXISTS VW_produtividade AS
           SELECT 
                prod.quantidade_produzida_estado,
                prod.ano,
                ROUND(prod.soma_produzida / col.area_colhida_soma, 2) AS produtividade
            FROM
                (SELECT 
                    SUBSTR(qp.municipio, -2) AS quantidade_produzida_estado,
                    ano,
                    SUM(produzida) AS soma_produzida
                FROM 
                    quantidade_produzida qp
                GROUP BY 
                    quantidade_produzida_estado, ano) AS prod
            JOIN
                (SELECT 
                    SUBSTR(ac.municipio, -2) AS area_colhida_estado,
                    ano,
                    SUM(colhida) AS area_colhida_soma
                FROM 
                    area_colhida ac 
                GROUP BY 
                    area_colhida_estado, ano) AS col
            ON 
                prod.quantidade_produzida_estado = col.area_colhida_estado
                AND prod.ano = col.ano;
        ''')
        conn.commit()

    def fetch_data(self, year, data_type):
        """
        Recupera dados da API do IBGE para o ano e tipo de área especificados.

        Parameters:
            year (int): Ano para recuperar os dados.
            data_type (int): Tipo de dados produzido/colhido”.

        Returns:
            dict: Dados recuperados da API do IBGE.
        """
        
        base_url = "https://apisidra.ibge.gov.br/values/t/5457/n6/all/v/{}/p/{}/c782/40124?formato=json"
        url = base_url.format(data_type, year)
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def insert_or_update(self, year):
        """
        Insere ou atualiza os dados de área colhida e produzida para o ano especificado no banco de dados.

        Parameters:
            year (int): Ano para o qual inserir ou atualizar os dados.
        """

        print("Iniciando a população das tabelas de área colhida e produzida")
        conn = self.create_connection(self.db_name)
        cursor = conn.cursor()

        area_data = self.fetch_data(year, 216)
        if area_data:
            date = [(entry['D1N'], entry['D1C'], entry['D3N'], entry['V']) for entry in area_data[1:]]

            cursor.executemany('''
            INSERT INTO area_colhida (municipio, codigo, ano, colhida) VALUES (?, ?, ?, ?);
            ''', date)

        quantidade_data = self.fetch_data(year, 214)
        print("Iniciando segunda tabela")
        if quantidade_data:
            date = [(entry['D1N'], entry['D1C'], entry['D3N'], entry['V']) for entry in quantidade_data[1:]]

            cursor.executemany('''
            INSERT INTO quantidade_produzida (municipio, codigo, ano, produzida) VALUES (?, ?, ?, ?);
            ''', date)
        conn.commit()
        conn.close()

        print("Populadas as tabelas de área colhida e produzida")

    def delete(self, year):
        """Deleta os dados do ano de cada tabela."""

        conn = self.create_connection(self.db_name)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM area_colhida WHERE ano = ?', (year,))
        cursor.execute('DELETE FROM quantidade_produzida WHERE ano = ?', (year,))

        conn.commit()
        conn.close()


