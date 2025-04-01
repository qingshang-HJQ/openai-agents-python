import  os
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv
import httpx
# ------------------------------代码------------------------------
# 旅游智能体
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, ModelSettings, handoff
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
import asyncio
import json
from pydantic import BaseModel, ValidationError

from src.agents import gen_trace_id, trace
from src.agents.mcp import MCPServerStdio

#中文注释
load_dotenv()  # load environment variables from .env
http_client = httpx.AsyncClient(verify=False)
openai_client = AsyncOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-5d0df6fb5e864785947f2e4b60adb763",
    http_client=http_client
)

async def run(mcp_server: MCPServerStdio,):
        agent = Agent(
            name="问答智能体",
            instructions="""
            你是一个问答智能体，你将阅读本地文件，回答用户的问题。。
        
            你的任务是：
            1、当你需要时打开本地文件时，调用工具阅读本地文件。
            2、并以markdown 的格式输出问题。
            """,
            model=OpenAIChatCompletionsModel(
                model="qwen-72b-chat",
                openai_client=openai_client
            ),
            mcp_server=[mcp_server]


        )
        # List the files it can read
        message = "今天天气怎么样？"
        print(f"Running: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)

# MCPClient类
async def main(path):
    async with MCPServerStdio(
            name="Filesystem Server, via npx",
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", path],
            },
    ) as server:
        await run(server)

if __name__ == "__main__":
    asyncio.run(main("E:\PycharmProjects\openai-agents-python\examples\AI customer_service\mcp\test.txt"))