from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from dotenv import load_dotenv
import asyncio


load_dotenv()


async def main() -> None:
    server_params = StdioServerParams(
        command="/Users/josh/.local/bin/uv",
        args=[
            "run",
            "--directory",
            "../../",
            "--with",
            "mcp[cli]",
            "mcp",
            "run",
            "main.py",
        ],
    )

    # Get all available tools from the server
    tools = await mcp_server_tools(server_params)
    print("Tools discovered:", [f"{t.name}: {t.description}" for t in tools])

    # Create an agent that can use all the tools
    agent = AssistantAgent(
        name="researcher",
        model_client=OpenAIChatCompletionClient(model="gpt-4o-mini"),
        tools=tools,  # type: ignore
        reflect_on_tool_use=True,
    )

    # The agent can now use any of the Reddit tools
    result = await agent.run(
        task="Find some interesting posts on Reddit about AI agents",
        cancellation_token=CancellationToken(),
    )
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(main())
