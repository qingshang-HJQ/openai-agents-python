import os

from customer_service.RAG.file_parser import parse_file_and_embed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
async  def upload_file(fileinfo,body):
    """解析上传的文件并切割为向量"""
    result = None
    filename = fileinfo.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, 'wb') as f:
        f.write(fileinfo.body)

    result = await parse_file_and_embed(filepath)
