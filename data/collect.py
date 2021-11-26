import requests
from redditcleaner import clean

BASE_URL = 'http://api.reddit.com'
USER_AGENT = {'User-agent': 'two-solitudes-project'}

def save_comments_to_file(subreddit, min_amount, post_sort, post_timeframe, comment_sort, 
                    filename=None, max_comments_per_post=20):
    if not filename:
        filename = f'{subreddit}-{post_sort}_posts-{min_amount}_{comment_sort}_comments.txt'

    post_ids = []
    comment_count = 0
    while comment_count < min_amount:
        last_post = f't3_{post_ids[-1]}' if len(post_ids) != 0 else ''
        next_100_posts = requests.get(f'{BASE_URL}/r/{subreddit}/{post_sort}',
                                        params={'after': last_post,
                                                'timeframe': post_timeframe,
                                                'limit': 100},
                                        headers=USER_AGENT)\
                                    .json()['data']['children']
        for _post in next_100_posts:
            post = _post['data']
            post_ids.append(post["id"])
            comment_count += post['num_comments'] if post['num_comments'] < max_comments_per_post \
                                            else max_comments_per_post

    # TODO: this does not handle replies!!! If I'm not going to do that, set the depth to 1 to speed things up.
    comments = []
    for post_id in post_ids:
        post_comments = requests.get(f'{BASE_URL}/r/{subreddit}/comments/{post_id}',
                                    params={'limit': max_comments_per_post,
                                            'sort': comment_sort},
                                    headers=USER_AGENT) \
                                .json()
        post_comments = [comment['data']['children'][0] for comment in post_comments
                        if len(comment['data']['children']) > 0]
        comments.extend([clean(comment['data']['body']) for comment in post_comments \
                                    if comment['kind'] == 't1'])
    with open(filename, 'w') as fp:
        fp.write('\n'.join(comments))
    
if __name__ == "__main__":
    save_comments_to_file('Quebec', 100, 'new', 'all', 'top', max_comments_per_post=3)