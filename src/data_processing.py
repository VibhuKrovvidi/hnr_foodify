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

# global vars
default_corpus = {
  'food': ['pasta', 'food', 'drink', 'cocktails', 'pizza', 'roti', 'naan', 'noodles', 'burger', 'buns', 'bread', "soup"],
  'service': ['service', "waiter", 'plate', 'delivery', 'manager', 'staff', 'chef', 'chefs'],
  'price': ['price', 'value', 'cheap', 'expensive', 'bargain', 'deal', 'money', 'affordable', 'pricey'],
  'ambience': ['light', 'table', 'carpet', 'decoration', 'view', 'ambience'],
  'location' : ['area', 'location', 'destination', 'place'],
}

def process_for_restaurant(restaurant_name, current_corpus=default_corpus):
    # NOTE: reading from such a massive file is a very costly operation, can improve later
    df = pd.read_csv("scraped_output.csv")
    df.dropna(inplace=True)
    df.filter(df['Restaurant'] == restaurant_name)

    # Apply function to get feature-descriptors
    df["feature_descriptors"] = df["Review"].apply(lambda x:get_feature_descriptors(x))

    # Get sentiment
    df["sentiment_feat"] = df["feature_descriptors"].apply(lambda x:get_review_level_sentiment(x))

    # insert commented out code? NOTE: Ask Vibhu 

    # Then, find word vector
    embeddings_index = {}
    with open('glove.6B.100d.txt', encoding="utf8") as f:
        for line in f:
            word, coefs = line.split(maxsplit=1)
            coefs = np.fromstring(coefs, "f", sep=" ")
            embeddings_index[word] = coefs

    print("Found %s word vectors." % len(embeddings_index))

    vect_corpus = {
        aspect:[] for aspect in current_corpus
    } # modified to account for custom corpus

    for key in current_corpus.keys():
        arr = current_corpus[key]
        for word in arr:
            vect_corpus[key].append(embeddings_index[word])
        vect_corpus[key] = np.average(vect_corpus[key], axis=0)

    # final step 
    df["categorised_sentiment"] = df["sentiment_feat"].apply(lambda x:categorise(x, current_corpus, vect_corpus, embeddings_index))

    li = get_avg_polarity(df)
    print(li)
    return li;



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

def recalculate(vect_corpus, key):
  # Calculate avg
  vect_corpus[key] = np.average(vect_corpus[key], axis=0)
  return vect_corpus

def categorise(feat, current_corpus, vect_corpus, embeddings_index):
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
      for aspect in current_corpus.keys():
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
    
  return [retdict]

def get_avg_polarity(df):
        
    restaurants = df["Restaurant"].unique()
    restaurants = list(restaurants)

    avg_sent_list = []

    for rest in restaurants:
        tdf = df[df["Restaurant"] == rest]

        rmap = dict()

        ser = tdf["categorised_sentiment"].tolist()
        # print(ser)
        # break
        ser = [item for sublist in ser for item in sublist]
        # print(ser)
        # break
        
        for d in ser:
            for key in d.keys():
                if key in rmap:
                    for v in d[key]:
                        rmap[key].append(v)
                else:
                    rmap[key] = d[key]

        #     rmap.update(d)
        
        for key in rmap.keys():
            if len(rmap[key]) > 0:
                m = mean(rmap[key])
                rmap[key] = m
        # print(rmap)
        avg_sent_list.append((rest, rmap))

    return avg_sent_list

process_for_restaurant("Art")