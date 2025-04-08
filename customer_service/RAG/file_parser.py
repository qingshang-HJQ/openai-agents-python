
from customer_service.RAG.embedding_model import embed_texts
from customer_service.RAG.vector_store import store_vectors
import os
import fitz  # PyMuPDF，处理 PDF
import docx
import csv

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        doc = fitz.open(filepath)
        return "\n".join([page.get_text() for page in doc])
    elif ext == ".docx":
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    elif ext == ".csv":
        with open(filepath, encoding="utf-8") as f:
            reader = csv.reader(f)
            return "\n".join([", ".join(row) for row in reader])
    else:
        return ""

async def parse_file_and_embed(filepath: str, splitter_type: str = "regex"):
    """
    主入口：解析文件 -> 切分文本 -> 生成向量 -> 存入向量库
    """
    raw_text = extract_text(filepath)


    chunks = split_text(raw_text, splitter_type)
    vectors, meta = await generate_embeddings(chunks)
    save_vectors_to_faiss(vectors, meta, filepath)
    return {"chunks": len(chunks), "vectors": len(vectors)}
