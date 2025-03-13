from datetime import datetime
from .reddit_client import RedditClient
from .wrap_error import wrap_error
from util.date_utils import format_utc_timestamp


def search_subreddits_by_name(
    query: str,
    include_nsfw: bool = False,
    exact_match: bool = False,
):
    """Search for subreddits whose names begin with query."""
    client = RedditClient.get_instance()

    def execute():
        return [
            {
                "name": subreddit.display_name,
                "public_description": subreddit.public_description,
                # "description": subreddit.description,
                "url": subreddit.url,
                "subscribers": subreddit.subscribers,
                "created_utc": format_utc_timestamp(subreddit.created_utc),
            }
            for subreddit in client.reddit.subreddits.search_by_name(
                query, exact=exact_match, include_nsfw=include_nsfw
            )
        ]

    return wrap_error(execute)


def search_subreddits_by_description(query: str):
    """Search for subreddits by name or description."""
    client = RedditClient.get_instance()

    def execute():
        return [
            {
                "name": subreddit.display_name,
                "public_description": subreddit.public_description,
                # "description": subreddit.description,
                "url": subreddit.url,
                "subscribers": subreddit.subscribers,
                "created_utc": format_utc_timestamp(subreddit.created_utc),
            }
            for subreddit in client.reddit.subreddits.search(query)
        ]

    return wrap_error(execute)
