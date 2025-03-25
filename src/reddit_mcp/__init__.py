"""Reddit MCP - A plug-and-play MCP server to browse, search, and read Reddit."""

from importlib import metadata

__version__ = metadata.version("reddit-mcp")

from .tools.get_comments import get_comments_by_submission, get_comment_by_id
from .tools.get_submission import get_submission
from .tools.get_subreddit import get_subreddit
from .tools.search_posts import search_posts
from .tools.search_subreddits import search_subreddits

__all__ = [
    "get_comments_by_submission",
    "get_comment_by_id",
    "get_submission",
    "get_subreddit",
    "search_posts",
    "search_subreddits",
]
