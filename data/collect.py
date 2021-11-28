# import requests
# from redditcleaner import clean
from google.cloud import translate_v2 as translate
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

translate_client = translate.Client.from_service_account_json('creds.json')

# BASE_URL = 'http://api.reddit.com'
# USER_AGENT = {'User-agent': ''}

# TODO: improve verbosity over the the API request logging
def save_comments_to_file(subreddit, limit, post_sort, time_filter='all',
                    max_comments_per_post=50, filename=None, save_english_translation=False):
    if not filename:
        filename = f'data/{subreddit}-{post_sort}_posts-comments.txt'

    if post_sort == 'new':
        posts = reddit.subreddit(subreddit).new(limit=limit)
    elif post_sort == 'top':
        posts = reddit.subreddit(subreddit).top(limit=limit, time_filter=time_filter)
        # last_post = f't3_{post_ids[-1]}' if len(post_ids) != 0 else ''
        # next_100_posts = requests.get(f'{BASE_URL}/r/{subreddit}/{post_sort}',
        #                                 params={'after': last_post,
        #                                         'timeframe': timeframe,
        #                                         'count': len(post_ids),
        #                                         'limit': 100},
        #                                 headers=USER_AGENT)\
        #                             .json()['data']['children']
        # for _post in next_100_posts:
        #     post = _post['data']
        #     post_ids.append(post["id"])
        #     comment_count += post['num_comments'] if post['num_comments'] < max_comments_per_post \
        #                                     else max_comments_per_post
        # print(f'Got {len(post_ids)} posts')
        # if len(next_100_posts) < 100:
        #     break

    comments = []
    for num, post in enumerate(posts, start=1):
        print(f'Collecting comments for post {num}...')
        post.comment_sort = 'top'
        post.comments.replace_more(limit=None)
        collected = 0
        comment_queue = post.comments[:]
        while comment_queue and collected < max_comments_per_post:
            comment = comment_queue.pop(0)
            # TODO: why the heck are so many comment bodies empty
            if comment.body:
                comments.append(comment.body)
                collected += 1
            comment_queue.extend(comment.replies)
        print(f'{len(comments)} total comments collected')
        # post_comments = requests.get(f'{BASE_URL}/r/{subreddit}/comments/{post_id}',
        #                             params={'limit': max_comments_per_post,
        #                                     'sort': comment_sort},
        #                             headers=USER_AGENT) \
        #                         .json()
        # post_comments = [comment['data']['children'] for comment in post_comments
        #                 if len(comment['data']['children']) > 0]
        # for comment_list in post_comments:
        #     comments.extend([clean(comment['data']['body']) for comment in comment_list \
        #                             if comment['kind'] == 't1'])
        # print(f'Got {len(comments)} comments')

    with open(filename, 'w') as fp:
        fp.write('\n'.join(comments))

    # TODO: fix the error with the request payload size exceeds
    if save_english_translation:
        translated_comments = translate_client.translate(comments, target_language='en')
        with open(f'{filename}-EN', 'w') as fp:
            fp.write('\n'.join((translation["translatedText"] for translation in translated_comments)))

# TODO: time permitting, give this script command line args
if __name__ == "__main__":
    save_comments_to_file('Canada', 500, 'top', 'all')
    save_comments_to_file('onguardforthee', 500, 'top', 'all')
    save_comments_to_file('canadapolitics', 500, 'top', 'all')