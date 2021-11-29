from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from statistics import mean
import pandas as pd

from utils import get_data

sia = SentimentIntensityAnalyzer()
# https://realpython.com/python-nltk-sentiment-analysis/#using-nltks-pre-trained-sentiment-analyzer

# returns a dict with the average sentiment of sentences containing word accross dataset
def average_sentiment(dataset, words_or_stems):
    print('Tokenizing dataset...')
    sentences = []
    for comment in dataset:
        sentences.extend(sent_tokenize(comment))
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    print('Calculating sentiment polarities...')
    sentiments = {}
    for word_or_stem in words_or_stems:
        if ' ' in word_or_stem:
            sentences_with_word = [sentence for sentence in sentences if word_or_stem in sentence]
        else:
            sentences_with_word = [sentence for sentence, tokenized_sentence \
                                    in zip(sentences, tokenized_sentences) \
                                    if any(token.startswith(word_or_stem) for token in tokenized_sentence)]
        print(f'Found {len(sentences_with_word)} sentences with word/stem "{word_or_stem}"')
        scores = [sia.polarity_scores(sentence_with_word)['compound'] \
                    for sentence_with_word in sentences_with_word]
        sentiments[word_or_stem] = (round(mean(scores), 6), len(sentences_with_word))\
                             if scores else ('N/A', 0)
    return pd.DataFrame(sentiments.items(), columns=['word', 'average_sentiment_score/sentence_count'])

if __name__ == '__main__':
    words = ['secular', 'bill 21', 'bill 101', 'immigra', 'religio', 'tax',
             'quebec', 'canada', 'trudeau', 'legault', 'nationalis',
             'soverei', 'french', 'english', 'covid', 'vaccine', 'lockdown']
    QC_data, QC_no_mtl_data, ROC_data = get_data('QC'), get_data('QC', exclude=['montreal']), get_data('CA')
    QC_sentiments = average_sentiment(QC_data, words)
    QC_sentiments.to_csv('QC-sentiment.csv', index=False)
    QC_no_mtl_sentiments = average_sentiment(QC_no_mtl_data, words)
    QC_no_mtl_sentiments.to_csv('QC-no-mtl-sentiment.csv', index=False)
    ROC_sentiments = average_sentiment(ROC_data, words)
    ROC_sentiments.to_csv('ROC-sentiment.csv', index=False)