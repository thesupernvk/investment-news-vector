import psycopg2
import json
from vector_store.base import VectorStore

class PGVectorStore(VectorStore):

    def __init__(self, dsn: str):
        self.conn = psycopg2.connect(dsn)

    def add(self, ids, embeddings, documents, metadatas):
        with self.conn.cursor() as cur:
            for i in range(len(ids)):
                cur.execute("""
                    INSERT INTO documents (id, content, embedding, metadata)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """, (
                    ids[i],
                    documents[i],
                    embeddings[i],
                    json.dumps(metadatas[i])
                ))
        self.conn.commit()

    def similarity_search(self, query_embedding, k):
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT content, metadata
                        FROM documents
                        ORDER BY embedding <-> (%s)::vector
                LIMIT %s
                        """, (query_embedding, k))
            return cur.fetchall()

    def url_exists(self, url):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 1 FROM documents
                WHERE metadata->>'url' = %s LIMIT 1
            """, (url,))
            return cur.fetchone() is not None

    def content_hash_exists(self, content_hash):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 1 FROM documents
                WHERE metadata->>'content_hash' = %s LIMIT 1
            """, (content_hash,))
            return cur.fetchone() is not None
