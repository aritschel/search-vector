import re
from bs4 import BeautifulSoup
from sqlalchemy import text
from langchain.schema import Document
import postgres.db_connect as db_connect


def clean_text(html_content):
    """
    Remove HTML tags, extra spaces, and normalizes the text.

    Args:
        html_content (str): HTML content to be cleaned.

    Returns:
        str: Cleaned text.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
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


def get_documents_from_db():
    """
    Retrieve documents from the database.

    Returns:
        List[Document]: List of documents retrieved from the database.
    """
    session = db_connect.SessionLocal()
    try:
        result = session.execute(text("SELECT content FROM documents"))
        documents = [Document(page_content=row[0]) for row in result]
        return documents
    finally:
        session.close()


def split_text(text, chunk_size=300, overlap=50):
    """
    Splits the text into smaller chunks with overlap.

    Args:
        text (str): Text to be split.
        chunk_size (int): Size of each chunk.
        overlap (int): Overlap between chunks.

    Returns:
        list: List of text chunks.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks
