
from text2vec import SentenceModel
import asyncio

model = SentenceModel("shibing624/text2vec-base-chinese")  # 推荐：bge-base-zh

async def embed_texts(texts):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: model.encode(texts))
