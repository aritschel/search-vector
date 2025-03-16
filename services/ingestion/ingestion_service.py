from fastapi import FastAPI, HTTPException
import requests
import os
from services.database.db_manager import DBManager
from utils.embedding_processor import EmbeddingProcessor
from utils.text_processor import clean_text, split_text

app = FastAPI()
db = DBManager()
embeddings = EmbeddingProcessor()


@app.post("/fetch-web")
def fetch_and_store_webpage(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        cleaned_text = clean_text(response.text)
        text_chunks = split_text(cleaned_text)

        for chunk in text_chunks:
            embedding = embeddings.generate_embedding(chunk)
            db.insert_document(chunk, embedding)

        return {"message": "Trechos armazenados com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
