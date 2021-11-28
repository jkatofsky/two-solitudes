import praw
import logging

from secrets import ID, SECRET

reddit = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    user_agent="two-solitudes-project",
)

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# for logger_name in ("praw", "prawcore"):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(handler)

def save_comments_to_file(subreddit, limit, post_sort, time_filter='all',
                    max_comments_per_post=20, filename=None):
    if not filename:
        filename = f'data/{subreddit}-{post_sort}_posts-comments.txt'

    if post_sort == 'new':
        posts = reddit.subreddit(subreddit).new(limit=limit)
    elif post_sort == 'hot':
        posts = reddit.subreddit(subreddit).hot(limit=limit)
    elif post_sort == 'top':
        posts = reddit.subreddit(subreddit).top(limit=limit, time_filter=time_filter)
    comments = []
    for num, post in enumerate(posts, start=1):
        print(f'Collecting comments for post {num}...')
        post.comment_sort = 'top'
        # this was waaaay too slow to be useful
        # post.comments.replace_more(limit=max_comments_per_post)
        collected = 0
        comment_queue = post.comments[:]
        while comment_queue and collected < max_comments_per_post:
            comment = comment_queue.pop(0)
            # TODO: why the heck are so many comment bodies empty
            if not hasattr(comment, 'body') or len(comment.body) == 0:
                continue
            comments.append(comment.body.strip())
            collected += 1
            comment_queue.extend(comment.replies)
        print(f'{len(comments)} total comments collected')

    with open(filename, 'w') as fp:
        fp.write('\n'.join(comments))

# TODO: time permitting, give this script command line args
if __name__ == "__main__":
    save_comments_to_file('Canada', 500, 'hot')
    save_comments_to_file('onguardforthee', 500, 'hot')
    save_comments_to_file('canadapolitics', 500, 'hot')
    save_comments_to_file('Quebec', 500, 'hot')
    save_comments_to_file('montreal', 500, 'hot')
    save_comments_to_file('quebeccity', 500, 'hot')
    save_comments_to_file('quebeclibre', 500, 'hot')