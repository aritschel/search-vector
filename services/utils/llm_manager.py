import os
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv(".env")


class LLMManager:
    """
    Manages the configuration of the LLM and the generation of prompts.
    """

    def __init__(self):
        """
        Initialize the LLMManager with a specified HuggingFace model.
        """
        self.llm = HuggingFaceHub(
            repo_id="HuggingFaceH4/zephyr-7b-beta",
            model_kwargs={"temperature": 0.7, "max_length": 512},
            huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
        )

    def get_prompt(self, question, documents):
        """
        Generate the formatted prompt for the LLM.

        Args:
            question (str): The search question.
            documents (str): The documents to base the response on.

        Returns:
            str: The formatted prompt.
        """
        return (
            f"Baseando-se nos seguintes documentos encontrados:\n"
            f"{documents}\n"
            "Responda apenas com a resposta, sem repetir o enunciado ou mencionar os documentos.\n"
            "Sempre responda em português.\n"
            f"Pergunta: {question}"
        )

    def generate_response(self, question, documents):
        """
        Generate a response using the LLM.

        Args:
            question (str): The search question.
            documents (str): The documents to base the response on.

        Returns:
            str: The response generated by the LLM.
        """
        prompt = self.get_prompt(question, documents)
        response = self.llm(prompt)
        return (
            response.split("Resposta:")[-1].strip()
            if "Resposta:" in response
            else response.strip()
        )
