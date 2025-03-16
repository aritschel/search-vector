from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingProcessor:
    """
    Embedding processor class for generating embeddings using a HuggingFace model.
    """

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the EmbeddingProcessor with a specified model.

        Args:
            model_name (str): The name of the HuggingFace model to use for generating embeddings.
        """
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def generate_embedding(self, text):
        """
        Generate an embedding for the given text.

        Args:
            text (str): The text to generate an embedding for.

        Returns:
            list: The embedding vector.
        """
        return self.model.embed_documents([text])[0]
