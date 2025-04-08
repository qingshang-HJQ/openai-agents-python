# app/services/vector_store.py
import faiss
import os
import numpy as np
import pickle

INDEX_PATH = "faiss_index/index.bin"
META_PATH = "faiss_index/meta.pkl"

# 全局变量
index = faiss.IndexFlatL2(768)
meta = []

def store_vectors(texts, vectors):
    global index, meta
    vecs = np.array(vectors).astype("float32")
    index.add(vecs)
    meta.extend(texts)

    os.makedirs("faiss_index", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

def search_vector(query_vector, topk=5):
    D, I = index.search(np.array([query_vector]).astype("float32"), topk)
    return [meta[i] for i in I[0]]
