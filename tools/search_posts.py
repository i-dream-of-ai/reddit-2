from datetime import datetime
from typing import Literal
from .reddit_client import RedditClient
from .wrap_error import wrap_error
from util.date_utils import format_utc_timestamp


def search_posts(
    subreddit_name: str,
    query: str,
    sort: Literal["relevance", "hot", "top", "new", "comments"] = "relevance",
    syntax: Literal["cloudsearch", "lucene", "plain"] = "lucene",
):
    """Search for posts within a subreddit."""

    def execute():
        client = RedditClient.get_instance()
        subreddit = client.reddit.subreddit(subreddit_name)

        posts = subreddit.search(query=query, sort=sort, syntax=syntax)
        return [
            {
                "id": post.id,
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "num_comments": post.num_comments,
                "created_utc": format_utc_timestamp(post.created_utc),
            }
            for post in posts
        ]

    return wrap_error(execute)
