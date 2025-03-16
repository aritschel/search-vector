from fastapi import FastAPI, HTTPException
import requests
from services.database.db_manager import DBManager
from utils.embedding_processor import EmbeddingProcessor
from utils.text_processor import clean_text, split_text

app = FastAPI()
db = DBManager()
embeddings = EmbeddingProcessor()


@app.post("/fetch-web")
def fetch_and_store_webpage(url: str):
    """
    Fetches a webpage, cleans the text, splits it into chunks, and stores the chunks in the database.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        dict: A message indicating success or failure.

    Raises:
        HTTPException: If there is an error during the fetch or storage process.
    """
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
