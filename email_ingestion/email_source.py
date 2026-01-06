import os
from email_ingestion.eml_reader import read_eml
from email_ingestion.chunker import chunk_email


def fetch_email_newsletters(folder_path: str):
    """
    Fetch newsletters from a folder of .eml files
    """
    articles = []

    for file in os.listdir(folder_path):
        if not file.lower().endswith(".eml"):
            continue

        path = os.path.join(folder_path, file)
        email_doc = read_eml(path)

        chunks = chunk_email(email_doc["content"])

        for idx, chunk in enumerate(chunks):
            articles.append({
                "title": email_doc["title"],
                "link": file,
                "content": chunk,
                "metadata": {
                    **email_doc["metadata"],
                    "chunk_index": idx,
                    "total_chunks": len(chunks),
                    "filename": file
                }
            })

    return articles
