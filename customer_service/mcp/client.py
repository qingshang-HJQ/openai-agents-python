import  asyncio
import os
import shutil
import httpx
from agents import Agent, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI
from openai.lib.streaming.responses import ResponseTextDeltaEvent


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "file")
    http_client = httpx.AsyncClient(verify=False)
    openai_client = AsyncOpenAI(
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key="sk-5d0df6fb5e864785947f2e4b60adb763",
        http_client=http_client
    )
    # 创建一个mcp stdio servers
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        }
    ) as mcp_server_1:

        # 可以将MCP服务器添加到代理。每次代理运行时，代理SDK都会调用MCP服务器上的list_tools()。这使得LLM知道MCP服务器的工具。当LLM从MCP服务器调用工具时，SDK会调用该服务器上的call_tool()。
        agent = Agent(
            name="Assistant",
            instructions="Use the tools to achieve the task ",
            mcp_servers=[mcp_server_1],
            model=OpenAIChatCompletionsModel(
                model="qwen-72b-chat",
                openai_client=openai_client
            )

        )
        result = Runner.run_streamed(agent, input="Please tell me 5 jokes and save to test.txt")
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    # if not shutil.which("npx"):
    #     raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    asyncio.run(main())
