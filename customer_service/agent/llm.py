import httpx
from agents import AsyncOpenAI, OpenAIChatCompletionsModel


def llm_model():
    http_client = httpx.AsyncClient(verify=False)
    # 设置OpenAI客户端
    openai_client = AsyncOpenAI(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key="sk-5d0df6fb5e864785947f2e4b60adb763",
        http_client=http_client
    )

    llm_model = OpenAIChatCompletionsModel(
        model="qwen-72b-chat",
        openai_client=openai_client
    )
    return llm_model
