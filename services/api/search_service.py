from fastapi import FastAPI, HTTPException, Query
from services.database.db_manager import DBManager
from utils.embedding_processor import EmbeddingProcessor
from langchain_postgres.vectorstores import PGVector

app = FastAPI()
db = DBManager()
embeddings = EmbeddingProcessor()
vectorstore = PGVector(
    collection_name="documents", embeddings=embeddings.model, connection=db.conn_string
)


@app.get("/search")
def search_documents(query: str = Query(), k: int = 3):
    try:
        embedding = embeddings.generate_embedding(query)
        results = db.fetch_similar_documents(embedding, top_k=k)

        if not results:
            return {"message": "Nenhum resultado encontrado"}

        return {
            "results": [{"content": row[0], "similarity": row[1]} for row in results]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
