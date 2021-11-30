from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk import ngrams
import pandas as pd
from wordcloud import WordCloud

from utils import get_data

# import seaborn as sns
# import matplotlib.pyplot as plt

def word_frequency(dataset, top_n=500):
    sentence = " ".join(dataset)

    print("Tokenizing...")
    tokens = word_tokenize(sentence)
    lemmatizer = WordNetLemmatizer()

    print("Cleaning and lemmatizing...")
    tokens = [lemmatizer.lemmatize(t) for t in tokens
                    if t not in set(stopwords.words('english')) and t.isalpha()]

    print("Calculating frequencies...")
    noun_tokens = [word for (word, pos) in pos_tag(tokens) if pos[:2] == 'NN']
    nouns_freq = pd.DataFrame(FreqDist(noun_tokens).most_common(top_n), columns=['word', 'frequency'])
    bigrams = ngrams(tokens, 2)
    bigrams_freq = pd.DataFrame(FreqDist(bigrams).most_common(top_n), columns=['word', 'frequency'])

    return nouns_freq, bigrams_freq

def save_word_cloud(freq_file_path):
    df = pd.read_csv(freq_file_path)
    frequencies_dict = dict(zip(df.word, df.frequency))
    # 333f50
    wc = WordCloud(background_color="white", max_words=200, height=900, width=1600)
    wc.generate_from_frequencies(frequencies_dict)
    fn, _ = freq_file_path.split('.')
    wc.to_file(f'{fn}.png')

if __name__ == "__main__":
    # QC_data = get_data('QC', exclude=['montreal', 'quebeccity'])
    # QC_freq_nouns, QC_freq_bigrams = word_frequency(QC_data)
    # QC_freq_nouns.to_csv('quebec-no-cities-freq-nouns.csv', index=False)
    # QC_freq_bigrams.to_csv('quebec-no-cities-freq-bigrams.csv', index=False)

    # ROC_data = get_data('CA')
    # ROC_freq_nouns, ROC_freq_bigrams = word_frequency(ROC_data)
    # ROC_freq_nouns.to_csv('ROC-freq-nouns.csv', index=False)
    # ROC_freq_bigrams.to_csv('ROC-freq-bigrams.csv', index=False)
    # ROC_freq = word_frequency(get_data('ROC'))
    # print(ROC_freq)
    # fig, axes = plt.subplots(3, 1 ,figsize=(8,20))
    # sns.barplot(ax=axes[0], x='frequency', y='word', data=QC_freq.head(30))
    # sns.barplot(ax=axes[0], x='frequency', y='word', data=ROC_freq.head(30))

    save_word_cloud('frequency/QC-no-cities-freq-nouns.csv')
    save_word_cloud('frequency/ROC-freq-nouns.csv')