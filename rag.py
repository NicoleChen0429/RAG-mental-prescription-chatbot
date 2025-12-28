from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


STORE_DIR = Path("rag_store")
INDEX_FILE = STORE_DIR / "faiss.index"
CHUNKS_FILE = STORE_DIR / "chunks.npy"

# 多語向量模型（要跟 ingest.py 用同一個）
MODEL_NAME = "intfloat/multilingual-e5-base"


class RAGRetriever:
    def __init__(self):
        if not INDEX_FILE.exists() or not CHUNKS_FILE.exists():
            raise FileNotFoundError("找不到向量庫檔案，請先執行 python ingest.py")

        self.index = faiss.read_index(str(INDEX_FILE))
        self.chunks = np.load(str(CHUNKS_FILE), allow_pickle=True).tolist()
        self.model = SentenceTransformer(MODEL_NAME)

    def search(self, query: str, k: int = 3):
        # E5 模型建議 query 前綴
        q = "query: " + query.replace("\n", " ")
        q_emb = self.model.encode([q], normalize_embeddings=True).astype("float32")

        scores, ids = self.index.search(q_emb, k)
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            results.append({
                "score": float(score),
                "text": self.chunks[idx],
                "id": int(idx)
            })
        return results


if __name__ == "__main__":
    r = RAGRetriever()
    q = "我最近很迷惘，不知道人生的方向"
    res = r.search(q, k=3)
    for i, item in enumerate(res, 1):
        print(f"\n=== TOP {i} | score={item['score']:.4f} | id={item['id']} ===")
        print(item["text"])
