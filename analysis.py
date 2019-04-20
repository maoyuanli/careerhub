import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import string
import heapq


def process_words(raw, remove_punc=False, add_stopwords=False, stem=False):
    raw = str(raw).lower()
    if remove_punc:
        nopunc = [c for c in raw if c not in string.punctuation]
        raw = ''.join(nopunc)

    stopwords_list = []
    stopwords_list_en = set(stopwords.words('english'))
    stopwords_list_fr = set(stopwords.words('french'))
    stopwords_list.extend(stopwords_list_en)
    stopwords_list.extend(stopwords_list_fr)
    if add_stopwords:
        stopwords_list.extend(additional_stopwords())
    nostop = [w for w in raw.split() if w.lower() not in stopwords_list]
    if stem:
        stemmer = PorterStemmer()
        return ' '.join([stemmer.stem(t) for t in nostop])
    else:
        return ' '.join(nostop)


def additional_stopwords():
    stopwords_file = open('additional_stopwordsList.txt')
    return [w.lower().replace('\n', '') for w in stopwords_file.readlines()]


def word_weight(s):
    fdist = nltk.FreqDist(s.split())
    fdict = dict(fdist)
    wdict = {}
    for key in fdict.keys():
        wdict[key] = fdict[key] / max(fdict.values())
    return wdict


def sentence_score(sentences, word_weight_dict: dict):
    sent_score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            if word in word_weight_dict.keys():
                if sentence not in sent_score.keys():
                    sent_score[sentence] = word_weight_dict[word]
                else:
                    sent_score[sentence] += word_weight_dict[word]
    return sent_score


df = pd.read_json('data.json')
df.dropna(subset=['descr'], inplace=True)
df['descr_no_punc'] = df['descr'].apply(lambda x: process_words(x, remove_punc=True))
df['descr_sent_token'] = df['descr'].apply(lambda x: nltk.sent_tokenize(process_words(x)))
df['descr_word_wt'] = df['descr_no_punc'].apply(lambda x: word_weight(x))
df['descr_sent_score'] = df.apply(lambda df: sentence_score(df['descr_sent_token'], df['descr_word_wt']), axis=1)
df['descr_summ'] = df['descr_sent_score'].apply(lambda d: heapq.nlargest(3, d, key=d.get))
