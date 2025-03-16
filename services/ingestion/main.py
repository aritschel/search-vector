from fastapi import FastAPI, HTTPException
import psycopg2
import os
import uvicorn
import requests
from langchain_huggingface import HuggingFaceEmbeddings
import re
from bs4 import BeautifulSoup

app = FastAPI()

DB_NAME = os.getenv("POSTGRES_DB", "hotmart_db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except psycopg2.OperationalError as e:
        raise Exception(f"Erro ao conectar ao PostgreSQL: {str(e)}")


conn = connect_to_db()
cursor = conn.cursor()


def clean_text(html_content):
    """Remove tags HTML, espaços extras e normaliza o texto"""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_text(text, chunk_size=300, overlap=50):
    """Divide o texto em partes menores e com sobreposição"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks


@app.post("/fetch-web")
def fetch_and_store_webpage(url):
    try:
        # url = "https://hotmart.com/pt-br/blog/como-funciona-hotmart"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Erro ao buscar a página")

        cleaned_text = clean_text(response.text)
        text_chunks = split_text(cleaned_text)

        for chunk in text_chunks:
            embedding = embedding_function.embed_documents([chunk])[0]
            embedding_str = "[" + ",".join(map(str, embedding)) + "]"

            cursor.execute(
                "INSERT INTO documents (content, embedding) VALUES (%s, %s::vector)",
                (chunk, embedding_str),
            )

        conn.commit()
        return {"message": "Trechos armazenados com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
def shutdown():
    conn.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
