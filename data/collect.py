import requests
import json

BASE_URL = 'http://api.reddit.com'

def save_comments_to_file(subreddit, min_amount, post_sort, post_timeframe, comment_sort, 
                    filename=None, max_comments_per_post=20):
    if not filename:
        filename = f'{subreddit}-{post_sort}_posts-{min_amount}_{comment_sort}_comments'

    # https://www.jcchouinard.com/reddit-api-without-api-credentials/
    # https://www.reddit.com/dev/api/#GET_hot

    post_fullnames = []
    comment_count = 0
    while comment_count < min_amount:
        # TODO: make sure the after word when there's nothing in post_fullnames
        next_100_posts = requests.get(f'{BASE_URL}/r/{subreddit}/{post_sort} \
                                        ?after={post_fullnames[-1]} \
                                        &timeframe={post_timeframe} \
                                        &limit=100') \
                                .json()['data']['children']
        for post in next_100_posts:
            post_fullnames.append(f'{post["kind"]}_{post["id"]}')
            comment_count += post['num_comments'] if post['num_comments'] < max_comments_per_post \
                                            else max_comments_per_post

    # make API calls to post_fullnames
    # https://www.reddit.com/dev/api/#GET_comments_{article}
    # save to a dataframe and then to_csv() that? or just use vanilla Python?

if __name__ == "__main__":
    # TODO: call function appropriately
    pass