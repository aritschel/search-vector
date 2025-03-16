from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingProcessor:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def generate_embedding(self, text):
        return self.model.embed_documents([text])[0]
