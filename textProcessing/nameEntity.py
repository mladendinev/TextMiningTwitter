__author__ = 'mladen'

import nltk
import textPreprocessing

class nameEntity():
    def extractNameEntity(self):
        tokens = nltk.word_tokenize("I was diagnosed with schizophrenia in the US in 1938")
        tokens = nltk.pos_tag(tokens)
        tree = nltk.ne_chunk(tokens)
        tree.draw()


    def extractEntities(self, listTweets):
        results = []
        for tweet in listTweets:
            tweet = textPreprocessing.tokenizeText(tweet)
            tag = nltk.pos_tag(tweet)
            results.append(nltk.chunk.ne_chunk(tag))
        return results


if __name__== '__main__':
    n = nameEntity()
    n.extractNameEntity()