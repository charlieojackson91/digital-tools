#NLP
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


def categorise_speech(keyword):
    categorises = keyword.split('\n') # this is a list of keyword queries
    nouns = []
    adjectives = []
    verbs = []
    ticker = 0
    for iteration in categorises:
        ticker = ticker + 1
        iteration = iteration.strip()
        category = word_tokenize(iteration) # splits into words
        tagged = nltk.pos_tag(category) # splits into words with speech tag
        noun_count = 0
        adjective_count = 0
        verb_count = 0
        counter = 0
        for word,tag in tagged:
            counter = counter + 1
            if 'NN' in tag and noun_count == 0:
                nouns.append(word+"\n")
                noun_count = noun_count + 1
            if 'JJ' in tag and adjective_count == 0:
                adjectives.append(word+"\n")
                adjective_count = adjective_count + 1
            if 'VB' in tag and verb_count == 0:
                verbs.append(word+"\n")
                verb_count = verb_count + 1
            if noun_count == 0 and counter == len(tagged):
                if ticker == 1:
                    nouns.append('\n\n')
                else:
                    nouns.append('\n')
            if adjective_count == 0 and counter == len(tagged):
                if ticker == 1:
                    adjectives.append('\n\n')
                else:
                    adjectives.append('\n')
            if verb_count == 0 and counter == len(tagged):
                if ticker == 1:
                    verbs.append('\n\n')
                else:
                    verbs.append('\n')
    return nouns, adjectives, verbs
    

def classify_keywords(keywords,classifiers):
    keywords_list = keywords.split('\n') # this is a list
    classifier_list = classifiers.split('\n') # this is a list
    ticker = 0
    lst = []
    for keyword in keywords_list:
        keyword = keyword.strip()
        ticker = ticker + 1
        count = 0
        for classifier in classifier_list:
            classifier = classifier.strip()
            count = count + 1
            if classifier in keyword:
                lst.append(classifier+"\n")
                break
            if len(classifier_list) == count and ticker == 1:
                lst.append('\n\n')
                break
            if len(classifier_list) == count:
                lst.append('\n')
            else:
                continue
    return lst
