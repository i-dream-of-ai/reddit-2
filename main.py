from mcp.server.fastmcp import FastMCP
from tools import tools
import logging

logger = logging.getLogger("mcp")

mcp = FastMCP("Reddit")

for tool in tools:
    logger.info(f"Registering tool: {tool.__name__}")
    mcp.tool()(tool)

if __name__ == "__main__":
    logger.info("Starting MCP server...")
    mcp.run(transport="stdio")
