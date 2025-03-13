from .reddit_client import RedditClient
from .search_subreddits import (
    search_subreddits_by_name,
    search_subreddits_by_description,
)
from .get_subreddit import get_subreddit
from .search_posts import search_posts
from .get_submission import get_submission
from .get_comments import (
    get_comments_by_submission,
    get_comment_by_id,
)


print("search_subreddits_by_name", search_subreddits_by_name("computer"))
print("search_subreddits_by_description", search_subreddits_by_description("computers"))
print("get_subreddit", get_subreddit("ChatGPT"))
print("search_posts", search_posts("ChatGPT", "artificial intelligence"))
print(get_submission("1j66jbs"))
print(get_comments_by_submission("1j66jbs"))
print(get_comment_by_id("mgmk7d2"))

print(search_posts("content_creation", "content repurposing", "hot"))
