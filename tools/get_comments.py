from datetime import datetime
from .reddit_client import RedditClient
from .wrap_error import wrap_error
from util.date_utils import format_utc_timestamp


def comment_to_dict(comment):
    return {
        "id": comment.id,
        "body": comment.body,
        "author": None if comment.author is None else comment.author.name,
        "created_utc": format_utc_timestamp(comment.created_utc),
        "is_submitter": comment.is_submitter,
        "score": comment.score,
        "replies": [comment_to_dict(reply) for reply in comment.replies],
    }


def get_comments_by_submission(submission_id: str, replace_more: bool = True):
    """Retrieve comments from a specific submission."""

    def execute():
        client = RedditClient.get_instance()
        submission = client.reddit.submission(submission_id)
        if replace_more:
            submission.comments.replace_more()
        return [comment_to_dict(comment) for comment in submission.comments.list()]

    return wrap_error(execute)


def get_comment_by_id(comment_id: str):
    """Retrieve a specific comment by ID."""

    def execute():
        client = RedditClient.get_instance()
        return comment_to_dict(client.reddit.comment(comment_id))

    return wrap_error(execute)
