# Pipeline_Dados

## Atividade 1 - Processo de Pipeline de Dados

## Instalação de dependências

Para instalar as dependências, execute os seguintes comandos no mesmo diretório do `main.py` desta atividade.

### 1. Criar o Ambiente Virtual

```shell
python3 -m venv venv
```

### 2. Ativar o Ambiente Virtual

No linux:
```shell
source venv/bin/activate
```

No windows:
```cmd
venv\Scripts\activate
```

### 3. Instalação de dependências

```shell
pip install -r requirements.txt
```

## Descrição da implementação

O software implementado busca os dados da API do IBGE sobre área colhida e quantidade produzida por município e ano. Utilizando um banco de dados relacional SQLite. O software é composto pela seguinte classe:

- [AgricultureDB](Activity_1/AgricultureDB.py): Extraia os dados da API do IBGE e popula um banco SQLite.

## Exemplo de funcionamento

Deve-se executar o programa em AgricultureDB.py, para isso siga as seguintes instruções.

Dentro do diretório Activity_1, execute o seguinte comando:

```shell
python3 main.py
```

## Parametros do [config.ini](./config.ini) (aba `Agriculture`)

Na aba `Agriculture`, existem 3 parâmetros:

- start_year: ano de início para consulta na API. Ex:

```ini
start_year = 2018
```

- path_db: diretório onde o banco está:
```ini
path_db = ../agricultura.db
```

- debug_mode = 0: programa imprimirá informações diretamente no terminal durante a execução.
- debug_mode = true: programa irá gerar e exibir gráficos de barras como forma de debug, consumindo a view.
- debug_mode = false: programa não irá imprimir nenhuma informação no terminal durante a execução.

```ini
debug_mode = 0
```

## Atividade 2 - Integração de Serviços - Desenvolvimento de API

## Instalação de dependências

Para instalar as dependências, execute os mesmos passos da atividade anterior.

- 1. Criar o Ambiente Virtual
- 2. Ativar o Ambiente Virtual
- 3. Instalação de dependências

## Descrição da implementação

O software implementa uma API utilizando a estrutura do FastAPI em Python. Por meio dessa API, os usuários podem acessar informações armazenadas em um banco de dados. Os endpoints e métodos foram desenvolvidos para oferecer consultas e retornar dados conforme solicitado.

## Exemplo de funcionamento

Deve-se executar o programa em main.py, para isso siga as seguintes instruções.

Dentro do diretório Activity_2, execute o seguinte comando:

```shell
uvicorn main:app --reload
```

Agora basta acessar o navegador para consumir a API, segue alguns exemplos:

http://localhost:8000/harvested_area/1100015/2020

http://localhost:8000/productivity/2020/AC,AL,SP

http://localhost:8000/produced_quantity/1100015,1100023/2020,2021,2019


## Parametros do [config.ini](./config.ini) (aba `db`)

Na aba `db`, existem 1 parâmetro:

- path_db: diretório onde o banco está:
```ini
path_db = ../agricultura.db
```



