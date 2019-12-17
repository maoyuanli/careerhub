import heapq
import string
from collections import Counter
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import os
import sys
from scrapy.cmdline import execute
from utils.popup import Popup


class JobDescriptionCrawler:
    def __init__(self,  output):
        self.output = output

    def crawl(self):
        # pop = Popup()
        pop_input = input('please enter keywords with space between(e.g. "python developer") :')

        if pop_input is not None:
            keywords = pop_input.strip()
        else:
            keywords = ''

        if keywords != '':
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            try:
                os.remove(self.output)
            finally:
                execute(['scrapy', 'crawl', 'jobs', '-a', 'keywords={0}'.format(keywords), '-o', self.output])
        else:
            print('No Keyword Entered', 'Please restart and enter the keyword(s)')


class JobDescriptionETL:
    def __init__(self, source, output):
        self.source = source
        self.output = output

    def etl(self):
        df = pd.read_json(self.source)
        df.dropna(subset=['descr'], inplace=True)
        df['descr_no_punc'] = df['descr'].apply(lambda x: JobDescriptionETL.process_words(x, remove_punc=True))
        df['descr_sent_token'] = df['descr'].apply(lambda x: nltk.sent_tokenize(JobDescriptionETL.process_words(x)))
        df['descr_word_wt'] = df['descr_no_punc'].apply(lambda x: JobDescriptionETL.word_weight(x))
        df['descr_sent_score'] = df.apply(
            lambda df: JobDescriptionETL.sentence_score(df['descr_sent_token'], df['descr_word_wt']),
            axis=1)
        df['descr_summ'] = df['descr_sent_score'].apply(lambda d: heapq.nlargest(3, d, key=d.get))
        df['descr_add_stopword'] = df['descr'].apply(
            lambda x: JobDescriptionETL.process_words(x, remove_punc=True, add_stopwords=True))
        df['descr_top_words'] = df['descr_add_stopword'].apply(lambda x: JobDescriptionETL.top_words(x))

        result = df[['title', 'company', 'descr_top_words', 'descr_summ', 'link']]
        result.to_json(self.output, orient='records')

    # data cleaning function
    @staticmethod
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
            stopwords_list.extend(JobDescriptionETL.additional_stopwords())
        nostop = [w for w in raw.split() if w.lower() not in stopwords_list]
        if stem:
            stemmer = PorterStemmer()
            return ' '.join([stemmer.stem(t) for t in nostop])
        else:
            return ' '.join(nostop)

    # apply additional stopwords to the default nltk ones
    @staticmethod
    def additional_stopwords():
        stopwords_file = open(r'./resources/additional_stopwords.txt')
        return [w.lower().replace('\n', '') for w in stopwords_file.readlines()]

    @staticmethod
    def word_weight(s):
        fdist = nltk.FreqDist(s.split())
        fdict = dict(fdist)
        wdict = {}
        for key in fdict.keys():
            wdict[key] = fdict[key] / max(fdict.values())
        return wdict

    @staticmethod
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

    @staticmethod
    def top_words(s):
        words_list = s.split()
        counter = Counter(words_list)
        most_tuple = counter.most_common(10)
        most_list = [e[0] for e in most_tuple]
        return most_list
