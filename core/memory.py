import sqlite3
from sentence_transformers import SentenceTransformer
import numpy as np

class Memory:
    def __init__(self, db_path="stormy_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._init_db()
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # local

    def _init_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                text TEXT,
                embedding BLOB,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_memory(self, text):
        emb = self.encoder.encode(text)
        self.cursor.execute("INSERT INTO memories (text, embedding) VALUES (?, ?)",
                            (text, emb.tobytes()))
        self.conn.commit()

    def search(self, query, k=5):
        q_emb = self.encoder.encode(query)
        # Simple cosine similarity (in‑memory for demo)
        self.cursor.execute("SELECT id, text, embedding FROM memories")
        rows = self.cursor.fetchall()
        similarities = []
        for row in rows:
            emb = np.frombuffer(row[2], dtype=np.float32)
            sim = np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb))
            similarities.append((sim, row[1]))
        similarities.sort(reverse=True)
        return [text for _, text in similarities[:k]]
