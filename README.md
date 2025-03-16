# Search Vector

## Descrição
Este projeto é uma aplicação de busca que utiliza embeddings e modelos de linguagem para encontrar documentos relevantes e gerar respostas baseadas em consultas de usuários. A aplicação é composta por dois serviços principais: `api` e `ingestion`.

- **API Service**: Responsável por receber consultas de busca, encontrar documentos relevantes e gerar respostas usando o Zephyr-7B-Beta via HuggingFaceHub.
- **Ingestion Service**: Responsável por buscar páginas web, limpar e dividir o texto em partes menores, e armazenar esses trechos no pgvector, uma extensão vetorial do Postgrees.

## Estrutura do Projeto

```plaintext
search-vector/
├── services/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── search_service.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── ingestion_service.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── database/
│   │   ├── init.sql
│   │   └── db_manager.py
│   └── utils/
│       ├── __init__.py
│       ├── embedding_processor.py
│       ├── llm_manager.py
│       └── text_processor.py
├── .env
├── .gitignore
├── docker-compose.yml
├── README.md
└── exemplos/
    ├── curl.txt
    └── shell.sh
```

## Configuração
### **Pré-requisitos**
- Docker
- Docker Compose

### **Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```
POSTGRES_DB,
POSTGRES_USER,
POSTGRES_PASSWORD,
POSTGRES_HOST,
POSTGRES_PORT,
HUGGINGFACE_API_TOKEN,

```
Isso garante que a API do Hugging Face seja acessada corretamente.

### **Inicialização do Banco de Dados**
O banco de dados **PostgreSQL** será inicializado automaticamente com a extensão `vector` e a tabela `documents`, usando o script `init.sql`.

### **Construção e Execução dos Serviços**
Para construir e executar os serviços, use o Docker Compose:
```sh
docker-compose up --build -d
```
Isso iniciará os serviços `api_service` e `ingestion_service`.

## **Endpoints**
### **API Service**
#### **Buscar Documentos e Gerar Respostas**
**GET `/search`**: Busca documentos semelhantes à consulta e gera uma resposta usando o modelo de linguagem.

**Parâmetros:**
- `question` (str): A consulta de busca.
- `k` (int): O número de documentos semelhantes a serem buscados (padrão: 3).

**Exemplo de Uso:**
```sh
curl -X GET "http://localhost:8000/search?question=pergunta?" \
     -H "Content-Type: application/json"
```

### **Ingestion Service**
#### **Coletar e Processar Páginas Web**
**POST `/fetch-web`**: Busca uma página web, limpa o texto, divide em partes menores e armazena no banco de dados.

**Parâmetros:**
- `url` (str): A URL da página web a ser buscada.

**Exemplo de Uso:**
```sh
curl -X POST "http://localhost:8001/fetch-web" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://exemplo.com/artigo"}'
```

## **Exemplos**
### **Uso com cURL**
Veja o arquivo `exemplos/curl.txt` para um exemplo de uso com cURL.

### **Uso com Shell Script**
Veja o arquivo `exemplos/shell.sh` para um exemplo de uso com um script shell.


