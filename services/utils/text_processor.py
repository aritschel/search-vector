import re
from bs4 import BeautifulSoup


def clean_text(html_content):
    """Remove tags HTML e espaços extras."""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def split_text(text, chunk_size=300, overlap=50):
    """Divide texto em trechos menores com sobreposição."""
    words = text.split()
    return [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size - overlap)
    ]
