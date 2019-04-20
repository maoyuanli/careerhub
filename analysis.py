import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import string
import heapq


def processWords(raw, removePunc=False, addStopwords=False, stem=False):
    raw = str(raw).lower()
    if removePunc:
        nopunc = [c for c in raw if c not in string.punctuation]
        raw = ''.join(nopunc)
    stopwordsList = []
    stopwordsList_en = set(stopwords.words('english'))
    stopwordsList_fr = set(stopwords.words('french'))
    stopwordsList.extend(stopwordsList_en)
    stopwordsList.extend(stopwordsList_fr)
    if addStopwords:
        stopwordsList.extend(additionalStopwords())
    nostop = [w for w in raw.split() if w.lower() not in stopwordsList]
    if stem:
        stemmer = PorterStemmer()
        return ' '.join([stemmer.stem(t) for t in nostop])
    else:
        return ' '.join(nostop)


def additionalStopwords():
    stopwordsFile = open('additional_stopwordsList.txt')
    return [w.lower().replace('\n', '') for w in stopwordsFile.readlines()]


def wordWeight(s):
    fdist = nltk.FreqDist(s.split())
    fdict = dict(fdist)
    wdict = {}
    for key in fdict.keys():
        wdict[key] = fdict[key] / max(fdict.values())
    return wdict


def sentenceScore(sentences, wordWeightDict: dict):
    sentScore = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence):
            if word in wordWeightDict.keys():
                if sentence not in sentScore.keys():
                    sentScore[sentence] = wordWeightDict[word]
                else:
                    sentScore[sentence] += wordWeightDict[word]
    return sentScore


df = pd.read_json('data.json')
df.dropna(subset=['descr'], inplace=True)
df['descr_no_punc'] = df['descr'].apply(lambda x: processWords(x, removePunc=True))
df['descr_sent_token'] = df['descr'].apply(lambda x: nltk.sent_tokenize(processWords(x)))
df['descr_word_wt'] = df['descr_no_punc'].apply(lambda x: wordWeight(x))
df['descr_sent_score'] = df.apply(lambda df: sentenceScore(df['descr_sent_token'], df['descr_word_wt']), axis=1)
df['descr_summ'] = df['descr_sent_score'].apply(lambda d: heapq.nlargest(3, d, key=d.get))
