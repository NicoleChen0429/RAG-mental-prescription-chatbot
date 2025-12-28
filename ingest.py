from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DATA_FILE = Path("data/self_talk.txt")
OUT_DIR = Path("rag_store")
OUT_DIR.mkdir(exist_ok=True)

def split_blocks(text: str):
    # 用「空行」切段，保留原始段落格式
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    # 過濾太短（避免空段或雜訊）
    parts = [p for p in parts if len(p) >= 20]
    return parts

def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError("找不到 data/self_talk.txt，請先建立並貼上你的籤詩內容。")

    raw = DATA_FILE.read_text(encoding="utf-8")
    chunks = split_blocks(raw)

    # 多語向量模型（中英文都可）
    model = SentenceTransformer("intfloat/multilingual-e5-base")

    # E5 模型建議加前綴：query: / passage:
    passages = ["passage: " + c.replace("\n", " ") for c in chunks]

    emb = model.encode(passages, normalize_embeddings=True, show_progress_bar=True)
    emb = np.asarray(emb, dtype="float32")

    dim = emb.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine（因為 normalize）=> 用 inner product
    index.add(emb)

    faiss.write_index(index, str(OUT_DIR / "faiss.index"))
    np.save(OUT_DIR / "chunks.npy", np.array(chunks, dtype=object), allow_pickle=True)

    print("✅ 向量庫建立完成")
    print("chunks =", len(chunks))
    print("saved to =", OUT_DIR.resolve())

if __name__ == "__main__":
    main()
