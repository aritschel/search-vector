from fastapi import FastAPI, HTTPException
import os
import uvicorn
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain.schema import Document
import re

app = FastAPI()

DB_NAME = os.getenv("POSTGRES_DB", "hotmart_db")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

conn_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(conn_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_documents_from_db():
    """
    Retrieve documents from the database.

    Returns:
        List[Document]: List of documents retrieved from the database.
    """
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT content FROM documents"))
        documents = [Document(page_content=row[0]) for row in result]
        return documents
    finally:
        session.close()


def clean_text(text):
    """
    Remove special characters, links, extra spaces, and normalize the text.

    Args:
        text (str): Text to be cleaned.

    Returns:
        str: Cleaned text.
    """
    text = re.sub(r"http[s]?://\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9.,!? ]", "", text)
    return text


def preprocess_query(query: str) -> str:
    """
    Remove extra spaces and normalize punctuation in the query.

    Args:
        query (str): Query to be preprocessed.

    Returns:
        str: Preprocessed query.
    """
    query = query.strip()
    query = re.sub(r"\s+", " ", query)
    query = re.sub(r"[^\w\s]", "", query)
    return query


documents = get_documents_from_db()
vectorstore = PGVector.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="documents",
    connection=conn_string,
)


@app.get("/search")
def search_documents(query: str, k: int = 3, score_threshold: float = 0.6):
    """
    Search for the most relevant and shortest excerpts.

    Args:
        query (str): Search query.
        k (int): Number of results to return.
        score_threshold (float): Score threshold to consider a result relevant.

    Returns:
        dict: Search results.
    """
    query = preprocess_query(query)
    try:
        docs_with_scores = vectorstore.similarity_search_with_relevance_scores(
            query, k=k
        )
        results = []
        for doc, score in docs_with_scores:
            if score >= score_threshold:
                cleaned_text = clean_text(doc.page_content)
                results.append({"content": cleaned_text, "score": score})
        if not results:
            return {"message": "No relevant answers found."}
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
