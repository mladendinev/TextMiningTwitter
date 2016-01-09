# from __future__ import unicode_literals
__author__ = 'mladen'
from nltk.corpus import sentiwordnet
from nltk.corpus import wordnet as wn
import semanticFunc
from nltk.parse import stanford


def findAllIndexes(list, num):
    return filter(lambda a: list[a]==num, range(0,len(list)))

def negationDetection(tweet):
    parser = stanford.StanfordDependencyParser(model_path="/home/mladen/TextMiningTwitter/history/englishPCFG.ser.gz")
    verbTags = [u'VB', u'VBD',u'VBG',u'VBN',u'VBP',u'VBZ']
    # parser = stanford.DependencyGraph()
    tree = [list(parse.triples()) for parse in parser.raw_parse(tweet)][0]
    print tree
    print "-------------------------------------------"
    relations = [str(x[1]) for x in tree]
    print relations
    if "neg" in relations:
        negation =findAllIndexes(relations,'neg')
        # print negation
        for index in negation:
            # print tree[index][0]
            if len(set(verbTags) & set(tree[index][0]))>0 or len(set(verbTags) & set(tree[index][1]))>0:
                print "negation detected"


def encodeTupple(list):
    encoded = [[s.encode('utf8') for s in t] for t in list]
    return encoded


def findSynsets(text):
    tokens = semanticFunc.tokenizeText(text)
    for token in tokens:
       for synset in wn.synsets(token):
           for lemma in synset.lemmas():
               print lemma.name()
        # print "hypernym", wn.synset('iodine.n.01').hypernyms()

def findSimilarityInSynsets(text):
 pass