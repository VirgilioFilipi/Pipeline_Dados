# Teste-Veeries

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
path_db = ../db/agricultura.db
```

- debug_mode = 0: programa imprimirá informações diretamente no terminal durante a execução.
- debug_mode = true: programa irá gerar e exibir gráficos de barras como forma de debug, consumindo a view.
- debug_mode = false: programa não irá imprimir nenhuma informação no terminal durante a execução.

```ini
debug_mode = 0
```

### Perguntas adicionais relacionadas com a sua proposta
1. Você já utilizou algum orquestrador de processos? O seu processo está estruturado para ser executado automaticamente com uma periodicidade definida? Por exemplo, duas vezes por semana?

R: Sim, já utilizei o cron para agendar tarefas simples e recorrentes em sistemas Linux, também tenho conhecimento no Airflow, especialmente em um projeto que participei onde o Airflow foi o orquestrador de processos escolhido. No momento, o meu processo atual não está estruturado para ser executado automaticamente com uma periodicidade definida.

2. Conhece a ferramenta Airflow? Se sim, poderia nos explicar como seria possível integrar o seu processo com o Airflow?

R: Sim, integrar o seu processo com o Airflow envolve a criação de um DAG que define as etapas do seu processo, a configuração de tarefas para executar essas etapas, a definição de dependências entre as tarefas e a programação da execução do DAG conforme necessário.

3. Muitas fontes de dados são inconsistentes. Assim, é possível que dados incompletos, “sujos”, ou até mesmo incorretos entrem no banco de dados. Poderia nos explicar um pouco sobre como lidar com estas situações?

R: lidar com dados inconsistentes requer uma abordagem cuidadosa. Utilizando principalmente a biblioteca Pandas em Python, podemos adotar várias estratégias para lidar com essas situações:

- Limpeza de dados: Identificar e corrigir erros nos dados, como valores ausentes, duplicatas ou outliers.
- Padronização: Garantir que os dados sigam um formato consistente, convertendo tipos de dados, formatando datas e normalizando valores.
- Imputação de dados: Preencher valores ausentes com base em padrões conhecidos, como a média, mediana ou valor mais frequente. É importante escolher a estratégia adequada para não distorcer as características dos dados, especialmente em séries temporais.

É essencial adotar medidas que preservem a integridade dos dados, evitando a introdução de viés. Por exemplo, ao lidar com séries temporais com muitos valores nulos, é importante escolher cuidadosamente a estratégia para não comprometer os dados.


4. Se, ao invés de utilizar uma ‘view’ (requisito 2), fosse necessário utilizar uma ‘table’, sua implementação ou a sua estratégia seriam alteradas? Você tomaria alguma outra decisão no desenvolvimento?

R: sim, precisaria de uma tabela adicional para armazenar os dados de produtividade, algumas mudanças seriam necessárias como:

- Adicionar uma tabela extra para armazenar os dados de produtividade.

- Modificar o código para criar e manipular essa nova tabela em vez de uma visualização.

- Considerar o impacto no desempenho, manutenção e armazenamento.


## Atividade 2 – Integração de Serviços - Desenvolvimento de API

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
path_db = ../db/agricultura.db
```

### Perguntas adicionais relacionadas com a sua proposta

1. Você já hospedou algum serviço web (específico para ser usado como backend) utilizando a nuvem?

R:Não, não exatamente um serviço web backend, mas sim um serviço de armazenamento no S3 com Parquet.


2. Você conhece Terraform? Se sim, poderia nos explicar como seria possível disponibilizar esta API usando o Terraform e uma “plataforma de nuvem” de sua escolha?

R: Já ouvi falar do Terraform, mas nunca utilizei ele.

3. Você conhece formas de autenticação e autorização para API? Poderia nos explicar como isso poderia ser implementado na sua proposta?

R:
- Autenticação de senha: os usuários autenticam-se fornecendo suas credenciais de login, como nome de usuário e senha
- Autenticação do token da API: os usuários autenticam-se fornecendo um token de acesso único, que é obtido por meio de um processo de autenticação prévio. Esse token é incluído nas requisições feitas à API para autenticar o acesso do cliente.



