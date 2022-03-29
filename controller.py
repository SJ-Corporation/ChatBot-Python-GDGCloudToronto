# Chat Bot program:

from newspaper import Article
import docx
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#Download the punkt package
nltk.download('punkt' , quiet=True)

#Get the Data
# data = Article('https://1drv.ms/w/s!Aov-9ONr3eTaqM9jqcEYbY8L0d9MjQ?e=hmNEVg')
data = docx.Document('https://1drv.ms/w/s!Aov-9ONr3eTaqM9jqcEYbY8L0d9MjQ?e=hmNEVg')
data.download()
data.parse()
data.nlp()
corpus = data.text

f = open('index.html' , 'a')

f.write(corpus)
f.close()