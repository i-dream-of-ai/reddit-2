from .reddit_client import RedditClient
from .wrap_error import wrap_error


def get_submission(submission_id: str):
    """Retrieve a specific submission by ID."""

    def execute():
        client = RedditClient.get_instance()
        submission = client.reddit.submission(submission_id)

        return {
            "title": submission.title,
            "url": submission.url,
            "author": submission.author,
            "subreddit": submission.subreddit.display_name,
            "score": submission.score,
            "num_comments": submission.num_comments,
            "selftext": submission.selftext,
            "created_utc": submission.created_utc,
        }

    return wrap_error(execute)
