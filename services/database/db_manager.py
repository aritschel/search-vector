from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


class DBManager:
    """
    Database manager class for handling database operations.
    """

    load_dotenv(".env")

    def __init__(self):
        """
        Initialize the DBManager with database connection details.
        """
        self.DB_NAME = os.getenv("POSTGRES_DB")
        self.DB_USER = os.getenv("POSTGRES_USER")
        self.DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.DB_HOST = os.getenv("POSTGRES_HOST")
        self.DB_PORT = os.getenv("POSTGRES_PORT")

        self.conn_string = (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        self.engine = create_engine(self.conn_string)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """
        Get a new database session.

        Returns:
            Session: A new SQLAlchemy session.
        """
        return self.Session()

    def insert_document(self, content, embedding):
        """
        Insert a document into the database.

        Args:
            content (str): The content of the document.
            embedding (list): The embedding vector of the document.
        """
        session = self.get_session()
        session.execute(
            text(
                "INSERT INTO documents (content, embedding) VALUES (:content, :embedding)"
            ),
            {"content": content, "embedding": embedding},
        )
        session.commit()
        session.close()

    def fetch_similar_documents(self, embedding, top_k=3):
        """
        Fetch documents similar to the given embedding.

        Args:
            embedding (list): The embedding vector to compare.
            top_k (int): The number of top similar documents to fetch.

        Returns:
            list: List of similar documents with their content and similarity score.
        """
        session = self.get_session()
        result = session.execute(
            text(
                """
                SELECT content, embedding <=> CAST(:embedding AS vector) AS similarity
                FROM documents
                ORDER BY similarity ASC
                LIMIT :top_k
                """
            ),
            {"embedding": embedding, "top_k": top_k},
        ).fetchall()
        session.close()
        return result
