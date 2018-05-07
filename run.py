import numpy as np
np.set_printoptions(threshold=np.inf)
from sklearn.model_selection import train_test_split
import pandas as pd
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
          "penang" : "penang",
          "putrajaya" : "putrajaya",
          "sabah" : "sabah",
          "sarawak" : "sarawak",
          "selangor" : "selangor",
          "terengganu" : "terengganu",
          "wilayah persekutuan kuala lumpur" : "wilayah persekutuan kuala lumpur",
          "johor bharu" : "johor bharu",
          "johor bahru" : "johor bahru",
          }

houseNo = {"block" : "block",
           "blok" : "blok",
           "blk" : "blk",
           "lot" : "lot",
           "no" : "no",
           "unit" : "unit",
           "lantai": "lantai",
           "peti" : "peti",
           "aras" : "aras",
           "floor" : "floor"}

cities = {"george town" : "george town",
          "ipoh" : "ipoh",
          "kuching" : "kuching",
          "kota kinabalu" : "kota kinabalu",
          "shah alam" : "shah alam",
          "melaka" : "melaka",
          "malacca" : "malacca",
          "alor setar" : "alor setar",
          "miri" : "miri",
          "petaling jaya" : "petaling jaya",
          "iskandar puteri" : "iskandar puteri",
          "seremban" : "seremban"}
country = {"malaysia" : "malaysia"}



#dataset = pd.read_csv('Address Format - Components.csv')
##X = dataset.iloc[:, [0]].values
##X = [X[i][0].split(",") for i in range(len(X))]
#X = dataset.iloc[:, 1:8]
#X['postcode'] = X['postcode'].fillna(0).astype(int)
#data = []
#for i in range(len(X)):
#    data.append([])
#    for j in range(0,7):
#        if str(X.values[i][j]) != 'nan' and X.values[i][j] != 0:
#            data[i].append((str(X.values[i][j]), X.columns[j]))

def word2features(sent, i):
    segment = sent[i][0]

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
        'segment.isHouseNo=%s' % isHouseNo(segment),
        'segment.isHouse=%s' % isHouse(segment),
        'segment.isCity=%s' % isCity(segment),
        'segment.isCity=%s' % isCountry(segment),
    ]
    if i > 0:
        segment1 = sent[i-1][0]
        features.extend([
            '-1:segment.lower=' + segment1.lower(),
            '-1:segment.istitle=%s' % segment1.istitle(),
            '-1:segment.isupper=%s' % segment1.isupper(),
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        segment1 = sent[i+1][0]
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
    return [label for i in range(len(sent)) for token, label in sent[i]]

def sent2tokens(sent):
    return [token for token in sent]

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

def isCity(sent):
    for k in cities:
        if k in sent.lower():
            return True
    return False
def isCountry(sent):
    for k in country:
        if k in sent.lower():
            return True
    return False

def isPostCode(sent):
    if re.search('[0-9]{4,5}$',sent):
        return True
    else:
        return False
    
    
def isHouseNo(sent):
    for k in houseNo:
        if k in sent.lower():
            return True
        if re.search('^[0-9]+$',sent):
            return True
    return False

def isHouse(sent):
    if re.search('^[A-Za-z]+$',sent):
            return True
    return False


def segmentSentence(sentence):
    sent = sentence.replace(", ", ",")
    sent = sent.split(",")
    sent1 = []
    sent1.append([])
    for i in range(len(sent)):
        sent1.append([])
        sent1[i].append([sent[i]])
    return sent1

#X = sent2features(data)
#Y = sent2labels(data)
#
#
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

def parseAddress(address):
    import pycrfsuite
    tagger = pycrfsuite.Tagger()
    tagger.open('crf.model')
    segSent = segmentSentence(address)
    prediction = tagger.tag(sent2features(segSent))
    components = {}
    for i in range(len(prediction)):
        components.update({segSent[i][0][0] : prediction[i]})
    return components
#trainer = pycrfsuite.Trainer(algorithm='l2sgd', verbose=True)
#
#for xseq, yseq in zip(X_train, y_train):
#    trainer.append([xseq], [yseq])
#
#trainer.set_params({
#
#    # coefficient for L2 penalty
#    'c2': 0.01,  
#
#    # maximum number of iterations
#    'max_iterations': 200,
#
#    # whether to include transitions that
#    # are possible, but not observed
#    'feature.possible_transitions': True
#})
#trainer.train('crf.model')



#y_pred = [tagger.tag([xseq]) for xseq in X_test]
#
#
#for x, y in zip(y_pred, [x[1].split("=")[1] for x in X_test]):
#    print("%s (%s)" % (y, x[0]))


# test = "No. 39 ,Jln 1/2, Seksyen 1,46000, Malaysia"
# print(parseAddress(test))
