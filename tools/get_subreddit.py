from .reddit_client import RedditClient
from .wrap_error import wrap_error


def get_subreddit(subreddit_name: str):
    """Retrieve a subreddit by name."""

    def execute():
        client = RedditClient.get_instance()
        return client.reddit.subreddit(subreddit_name)

    return wrap_error(execute)
