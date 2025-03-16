from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os


class DBManager:
    def __init__(self):
        self.DB_NAME = os.getenv("POSTGRES_DB", "hotmart_db")
        self.DB_USER = os.getenv("POSTGRES_USER", "user")
        self.DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
        self.DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
        self.DB_PORT = os.getenv("POSTGRES_PORT", "5432")

        self.conn_string = (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        self.engine = create_engine(self.conn_string)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        return self.Session()

    def insert_document(self, content, embedding):
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
