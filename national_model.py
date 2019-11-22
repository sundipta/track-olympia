import re
import pickle

import pandas as pd
import numpy as np

import nltk
from nltk.corpus import stopwords

from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#load classifier trained on national congressional data
clf = joblib.load('lr_national.pkl') 

#load matrix transformer
transformer = TfidfTransformer()
loaded_vec = TfidfVectorizer(decode_error="replace",vocabulary=pickle.load(open("features.pkl", "rb")))

#load csv for transforming back to labels
categories=pd.read_csv('categories.csv', index_col=0)

def clean_text(texts):
    clean_words = []
    texts = re.sub("([^a-zA-Z])"," ", texts)
    words = texts.lower().split()
    stop_words = set(stopwords.words("english"))
    stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '},','concerning', 'addressing', 'regarding'])
    words = [w for w in words if not w in stop_words]
    clean_words.append(" ".join(words))
    return clean_words

def return_category(input):
	clean_input = clean_text(input)
	print(clean_input)
	input_features = transformer.fit_transform(loaded_vec.fit_transform(clean_input))
	predicted = clf.predict(input_features)
	predicted_category = categories.loc[predicted].iloc[:,0]
	return predicted_category