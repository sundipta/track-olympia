import os
import re

from gensim import corpora, models, similarities
from collections import defaultdict

from gensim.test.utils import common_corpus, common_dictionary, get_tmpfile
from gensim.models import LsiModel

import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from pprint import pprint  # pretty-printer

import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


engine = create_engine('sqlite:///bill_db.sqlite')
query = 'SELECT * FROM bill_info_table WHERE Active ORDER BY "level_0" ASC ;'
query_result=pd.read_sql_query(query,engine)
bill_info = query_result.set_index('level_0')
bill_info_subset = bill_info[~bill_info['LongDescription'].isnull()]

documents = bill_info_subset['LongDescription'].tolist()

stoplist = set('for a of the and to in or an is concerning addressing regarding'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

#tf-idf model
tfidf = models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

#lsi model
lsi = models.LsiModel(tfidf_corpus, num_topics=100, id2word=dictionary)
lsi_corpus = lsi[tfidf_corpus]
num=100

#get cosine similarity
index = similarities.MatrixSimilarity(lsi_corpus, num_features=num)

def vectorize(fromUser  = 'Default' ):
	vec_bow = dictionary.doc2bow(fromUser.lower().split())
	vec_lsi = lsi[vec_bow]
	sims = index[vec_lsi]
	sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
	top_ten = []
	for sim in sorted_sims[:20]:
	    if sim[1] >0.5:
		    bill_ID = bill_info_subset.iloc[sim[0]]['index']
		    top_ten.append((bill_ID, sim[1]))
		#print(bill_info_subset.iloc[sim[0]])
		#print(texts[sim[0]])
		#print('----')
	return top_ten
