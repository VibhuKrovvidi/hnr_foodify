# Imports
import pandas as pd
import numpy as np
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
en = spacy.load('en_core_web_sm')
en.add_pipe('spacytextblob')
import deplacy
import stanza
stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize, sentiment')
from statistics import mean
import xml.etree.ElementTree as ET
from scipy import spatial

# read raw reviews
df = pd.read_csv("scraped_output.csv")
df.dropna(inplace=True)

def get_feature_descriptors(text):
    doc = en(text)
    # deplacy.render(doc)
    words_seen = set()
    fd_dict = dict()
    for sent in doc.sents:
        for word in sent:
            if word.pos_ == "NOUN":
                temp_noun = word.text
                fd_dict[word.text] = [] # Empty list
            if word.pos_ in ["ADV", "ADJ", "VERB"]:
                try:
                    fd_dict[temp_noun].append(word.text)
                except:
                    pass
    return [fd_dict]

def get_review_level_sentiment(feat):
    feat = feat[0]
    comb_dict = dict()
    for key in feat.keys():
        arr = feat[key]
        if key in comb_dict:
            for word in arr:
                doc = nlp(word)
                for i, sentence in enumerate(doc.sentences):
                    # print(word, sentence.sentiment)
                    comb_dict[key].append(sentence.sentiment)
        else:
            comb_dict[key] = []
            for word in arr:
                doc = nlp(word)
                for i, sentence in enumerate(doc.sentences):
                    # print(word, sentence.sentiment)
                    comb_dict[key].append(sentence.sentiment-1)
    return [comb_dict]

# further process to categorise
corpus = {
  'food': ['pasta', 'food', 'drink', 'cocktails', 'pizza', 'roti', 'naan', 'noodles', 'burger', 'buns', 'bread', "soup"],
  'service': ['service', "waiter", 'plate', 'delivery', 'manager', 'staff', 'chef', 'chefs'],
  'price': ['price', 'value', 'cheap', 'expensive', 'bargain', 'deal', 'money', 'affordable', 'pricey'],
  'ambience': ['light', 'table', 'carpet', 'decoration', 'view', 'ambience'],
  'location' : ['area', 'location', 'destination', 'place'],
}

# Then, find word vector
embeddings_index = {}
with open('glove.6B.100d.txt', encoding="utf8") as f:
    for line in f:
        word, coefs = line.split(maxsplit=1)
        coefs = np.fromstring(coefs, "f", sep=" ")
        embeddings_index[word] = coefs

print("Found %s word vectors." % len(embeddings_index))

vect_corpus = {
    'food':[], 'service': [], 'price': [], 'ambience':[], 'location':[]
  }

for key in corpus.keys():
  arr = corpus[key]
  for word in arr:
    vect_corpus[key].append(embeddings_index[word])
  vect_corpus[key] = np.average(vect_corpus[key], axis=0)

def recalculate():
  # Calculate avg
  vect_corpus[key] = np.average(vect_corpus[key], axis=0)
  return vect_corpus

def categorise(feat):
  feat = feat[0]
  feat = feat.copy()
  # print(feat)
  retdict = dict()

  for key in feat.keys():
    try:
      vkey = embeddings_index[key]
      # print("VKEY", vkey, "=====\n\n")

      max_sim = -1
      cat = ""

      # Comp to each feature
      for aspect in corpus.keys():
        # Get cosine sim for each
        result = 1 - spatial.distance.cosine(vkey, vect_corpus[aspect])
    
        if result > max_sim:
          # print(result)
          max_sim = result
          cat = aspect
      if cat in retdict:
        for i in feat[key]:
          retdict[cat].append(i)

      else:
        retdict[cat] = feat[key]
      # print(retdict)
      # corpus[cat].append(key)
      # recalculate()
    except:
      pass
    
  return retdict