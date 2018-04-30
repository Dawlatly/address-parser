import numpy as np
np.set_printoptions(threshold=np.inf)
import matplotlib.pyplot as plt
import pandas as pd
import math
import re


roads = {"jalan" : "jalan", 
         "lorong" : "lorong",
         "persiaran" : "persiaran",
         "jln" : "jln",
         "lebuh" : "lebuh",
         "psn" : "psn",
         "lengkok" : "lengkok",
         "lebuhraya" : "lebuhraya",
         "lingkaran" : "lingkaran",
         "leboh" : "leboh",
         "lrg" : "lrg"}

states = {"johor" : "johor",
          "kedah" : "kedah",
          "kelantan" : "kelantan",
          "labuan" : "labuan",
          "melaka" : "melaka",
          "negeri sembilan" : "negeri sembilan",
          "pahang" : "pahang",
          "perak" : "perak",
          "perlis" : "perlis",
          "pinang" : "pinang",
          "putrajaya" : "putrajaya",
          "sabah" : "sabah",
          "sarawak" : "sarawak",
          "selangor" : "selangor",
          "terengganu" : "terengganu",
          "wilayah persekutuan kuala lumpur" : "wilayah persekutuan kuala lumpur",
          "johor bharu" : "johor bharu",
          }



dataset = pd.read_csv('Address Format - Components.csv')
#X = dataset.iloc[:, [0]].values
#X = [X[i][0].split(",") for i in range(len(X))]
X = dataset.iloc[:, 1:8]
data = []
for i in range(len(X)):
    for j in range(0,7):
        if not math.isnan(X.values[i][j]):
            data.append((X.values[i][j], X.columns[j]))
y = dataset.iloc[:, 1:8]

def word2features(sent, i):
    segment = sent[i]

    features = [
        'bias',
        'segment.lower=' + segment.lower(),
        'segment[-3:]=' + segment[-3:],
        'segment[-2:]=' + segment[-2:],
        'segment.isupper=%s' % segment.isupper(),
        'segment.istitle=%s' % segment.istitle(),
        'segment.isdigit=%s' % segment.isdigit(),
        'segment.isRoad=%s' % isRoad(segment),
        'segment.isState=%s' % isState(segment),
        'segment.isPostCode=%s' % isPostCode(segment),
    ]
    if i > 0:
        segment1 = sent[i-1]
        features.extend([
            '-1:segment.lower=' + segment1.lower(),
            '-1:segment.istitle=%s' % segment1.istitle(),
            '-1:segment.isupper=%s' % segment1.isupper(),
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        segment1 = sent[i+1]
        features.extend([
            '+1:segment.lower=' + segment1.lower(),
            '+1:segment.istitle=%s' % segment1.istitle(),
            '+1:segment.isupper=%s' % segment1.isupper(),
        ])
    else:
        features.append('EOS')
    return features


def sent2features(sent):
    return [word2features(sent[i], j)  for i in range(len(sent)) for j in range(len(sent[i]))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

def isRoad(sent):
    for k in roads:
        if k in sent.lower():
            return True
    return False

def isState(sent):
    for k in states:
        if k in sent.lower():
            return True
    return False

def isPostCode(sent):
    if re.search('[0-9]{4,5}$',sent):
        return True
    else:
        return False

sent2features(X)