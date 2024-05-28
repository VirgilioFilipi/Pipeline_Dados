from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import configparser
import sys
from typing import List, Dict, Union

app = FastAPI()

config = configparser.ConfigParser()
config.read('../config.ini')

if 'Agriculture' not in config:
    print("Seção 'Agriculture' não encontrada no arquivo config.ini")
    sys.exit(1)
try:
    path_db = config.get('db', 'path_db') 

except (configparser.NoOptionError, configparser.NoSectionError) as e:
    print(f"Erro ao ler configurações do arquivo config.ini: {e}")
    sys.exit(1)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

class APIResponse(BaseModel):
    success: bool
    data: Union[List[Dict[str, Union[str, float]]], None]
    message: str

@app.get("/harvested_area/{code}/{year}", response_model=APIResponse)
def get_harvested_area(code: str, year: int):
    """
    Retorna a área colhida de um determinado código de área e ano.

    Parâmetros:
    - code: Código da área a ser consultada (str).
    - year: Ano da colheita a ser consultada (int).
    
    Retorna:
    - JSON com os seguintes campos:
        - success: Indica se a operação foi bem-sucedida (bool).
        - data: Dados retornados (list of dict).
        - message: Mensagem de status (str).
    """
    conn = create_connection(path_db)
    cursor = conn.cursor()
    cursor.execute("SELECT colhida FROM area_colhida WHERE codigo = ? AND ano = ?", (code, year))
    result = cursor.fetchone()
    conn.close()

    if result:
        # Padronizar os dados retornados
        data = [{"colhida": result[0]}]
        return {"success": True, "data": data, "message": "Dados recuperados com sucesso."}
    else:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Dados não encontrados."})


@app.get("/productivity/{year}/{states}", response_model=APIResponse)
def get_productivity(year: int, states: str):
    """
    Retorna a produtividade por ano e estados específicos.

    Parâmetros:
    - year: Ano da produção a ser consultada (int).
    - states: Estados para os quais a produtividade será consultada, separados por vírgula (str).

    Retorna:
    - JSON com os seguintes campos:
        - success: Indica se a operação foi bem-sucedida (bool).
        - data: Dados retornados (list of dict).
            - estado: Nome do estado (str).
            - produtividade: Valor da produtividade (float).
        - message: Mensagem de status (str).
    """
    states_list = states.split(',')
    conn = create_connection(path_db)
    if conn is None:
        raise HTTPException(status_code=500, detail="Não foi possível conectar ao banco de dados.")
    
    cursor = conn.cursor()
    placeholders = ','.join('?' for _ in states_list)
    query = f"""
        SELECT quantidade_produzida_estado, produtividade 
        FROM VW_produtividade 
        WHERE ano = ? AND quantidade_produzida_estado IN ({placeholders})
    """
    try:
        cursor.execute(query, [year] + states_list)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {e}")
    
    conn.close()

    if results:
        data = [{"estado": row[0], "produtividade": row[1]} for row in results]
        return {"success": True, "data": data, "message": "Dados recuperados com sucesso."}
    else:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Dados não encontrados."})

@app.get("/produced_quantity/{code}/{year}", response_model=APIResponse)
def get_produced_quantity(code: str, year: str):
    """
    Retorna a quantidade produzida por código e ano específicos.

    Parâmetros:
    - code: Código ou lista de códigos de municípios a serem consultados, separados por vírgula (str).
    - year: Ano ou lista de anos para os quais a quantidade produzida será consultada, separados por vírgula (str).

    Retorna:
    - JSON com os seguintes campos:
        - success: Indica se a operação foi bem-sucedida (bool).
        - data: Dados retornados (list of dict).
            - municipio: Nome do município (str).
            - ano: Ano da produção (str).
            - produzida: Quantidade produzida (float).
        - message: Mensagem de status (str).
    """
    municipalities_list = code.split(',')
    years_list = year.split(',')

    if len(municipalities_list) * len(years_list) > 100:
        raise HTTPException(status_code=400, detail={"success": False, "data": None, "message": "Solicitação excede o limite de 100 dados."})

    conn = create_connection(path_db)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT municipio, ano, produzida 
        FROM quantidade_produzida 
        WHERE codigo IN ({}) AND ano IN ({})
    """.format(','.join('?' * len(municipalities_list)), ','.join('?' * len(years_list))), municipalities_list + years_list)
    result = cursor.fetchall()
    conn.close()

    if result:
        data = [{"municipio": row[0], "ano": row[1], "produzida": row[2]} for row in result]
        return {"success": True, "data": data, "message": "Dados recuperados com sucesso."}
    else:
        raise HTTPException(status_code=404, detail={"success": False, "data": None, "message": "Dados não encontrados."})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

