from google.cloud import translate_v2 as translate
import re
import os
import html

translate_client = translate.Client.from_service_account_json('creds.json')

def clean(comment):
    comment = comment.lower()
    comment = html.unescape(comment)
    return re.sub(r'http\S+', '', comment)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]

def clean_and_translate_file_contents(filename):
    with open(filename, 'r') as fp:
        comments = fp.readlines()
        comment_chunks = chunks(comments, 100)
        translated = []
        for comment_chunk in comment_chunks:
            translated_comments = translate_client.translate(comment_chunk, target_language='en')
            translated.extend((clean(translation["translatedText"]) for translation in translated_comments))
        fn, ext = filename.split('.')
        with open(f'{fn}-CLEAN.{ext}', 'w') as fp2:
            fp2.write('\n'.join(translated))

def make_merged_clean_file(directory):
    with open(f'{directory}/merged-CLEAN.txt', 'w') as outfile:
        for filename in [filename for filename in os.listdir(directory) if 'CLEAN' in filename]:
            with open(f'{directory}/{filename}') as infile:
                for line in infile:
                    outfile.write(line)

# TODO: setup with command line args
if __name__ == '__main__':
    # clean_and_translate_file_contents(f'data/CA/canadapolitics-hot_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/CA/canadapolitics-top_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/CA/onguardforthee-hot_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/CA/onguardforthee-top_posts-comments.txt')
    # for filename in os.listdir('data/QC'):
    #     clean_and_translate_file_contents(f'data/QC/{filename}')
    # clean_and_translate_file_contents(f'data/QC/montreal-top_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/montreal-hot_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/Quebec-top_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/Quebec-hot_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/quebeccity-top_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/quebeccity-hot_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/quebeclibre-top_posts-comments.txt')
    # clean_and_translate_file_contents(f'data/QC/quebeclibre-hot_posts-comments.txt')
    make_merged_clean_file('data/QC')
    make_merged_clean_file('data/CA')


