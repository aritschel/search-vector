import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


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

conn_string = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
engine = create_engine(conn_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
