import re
from bs4 import BeautifulSoup


def clean_text(html_content):
    """
    Remove HTML tags and extra spaces from the given HTML content.

    Args:
        html_content (str): The HTML content to be cleaned.

    Returns:
        str: The cleaned text.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def split_text(text, chunk_size=300, overlap=50):
    """
    Split the text into smaller chunks with overlap.

    Args:
        text (str): The text to be split.
        chunk_size (int): The size of each chunk.
        overlap (int): The overlap between chunks.

    Returns:
        list: List of text chunks.
    """
    words = text.split()
    return [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]
