import requests
from redditcleaner import clean

BASE_URL = 'http://api.reddit.com'
USER_AGENT = {'User-agent': 'two-solitudes-project'}

def save_comments_to_file(subreddit, min_amount, post_sort, comment_sort, 
                    filename=None, max_comments_per_post=20):
    if not filename:
        filename = f'{subreddit}-{post_sort}_posts-{min_amount}_{comment_sort}_comments.txt'

    post_ids = []
    comment_count = 0
    while comment_count < min_amount:
        last_post = f't3_{post_ids[-1]}' if len(post_ids) != 0 else ''
        next_100_posts = requests.get(f'{BASE_URL}/r/{subreddit}/{post_sort}',
                                        params={'after': last_post,
                                                'limit': 100},
                                        headers=USER_AGENT)\
                                    .json()['data']['children']
        for _post in next_100_posts:
            post = _post['data']
            post_ids.append(post["id"])
            comment_count += post['num_comments'] if post['num_comments'] < max_comments_per_post \
                                            else max_comments_per_post
        print(f'Got {len(post_ids)} posts')
        if len(next_100_posts) < 100:
            break

    # TODO: handle replies!!!
    comments = []
    for post_id in post_ids:
        post_comments = requests.get(f'{BASE_URL}/r/{subreddit}/comments/{post_id}',
                                    params={'limit': max_comments_per_post,
                                            'sort': comment_sort},
                                    headers=USER_AGENT) \
                                .json()
        post_comments = [comment['data']['children'] for comment in post_comments
                        if len(comment['data']['children']) > 0]
        for comment_list in post_comments:
            comments.extend([clean(comment['data']['body']) for comment in comment_list \
                                    if comment['kind'] == 't1'])
        print(f'Got {len(comments)} comments')
    with open(filename, 'w') as fp:
        fp.write('\n'.join(comments))

# TODO: give this script command line args?
if __name__ == "__main__":
    save_comments_to_file('Quebec', 1000, 'new', 'top')