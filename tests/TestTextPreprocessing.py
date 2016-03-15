# -*- coding: utf-8 -*-
__author__ = 'mladen'
import unittest
from textProcessing import textPreprocessing as process


def func(x):
    return x + 1


class TestTextPreprocessing(unittest.TestCase):
    def test_english_language(self):
        """Is five successfully determined to be prime?"""
        text = "@JacobWhitesides I'm learning about schizophrenia"
        self.assertEquals(process.detectLanguage(text), True)

    def test_spanish_language(self):
        text = u'después de mudarme a Madrid.'
        self.assertEquals(process.detectLanguage(text.encode("utf-8")), False)

    def test_cotains_links(self):
        text = 'Beyond the Big Name Brands. My piece with @HeinzMarketing http://t.co/gcL4PQDWhw #salesenablement @clicktotweet '
        self.assertEquals(process.containLinks(text.encode("utf-8")), True)

    def test_retweeted_links(self):
        text = u'RT #PreorderReflectionOniTunes and I will start following in a little'
        self.assertEquals(process.retweeeted(text), True)

    def test_remove_tweet_objects(self):
        text = u'RT @gamerdave69 @mattgallo123 this must be what causes schizophrenia'
        self.assertEquals(process.objectRemoval(text), "this must be what causes schizophrenia")

    def test_remove_stopwords(self):
        text = u'RT @gamerdave69 @mattgallo123 this must be what causes schizophrenia'
        self.assertEquals(process.removeStopwords(text), "RT @gamerdave69 @mattgallo123 must causes schizophrenia")

    def test_remove_emoji(self):
        text = u"I keep waking up at like 3 am starving and i fall back asleep because so the hungry \U0001f62d\U0001f62d\U0001f62d\U0001f62d"
        self.assertEquals(process.remove_emoji(text), "I keep waking up at like 3 am starving and i fall back asleep because so the hungry ")

    def test_remove_punctuation(self):
        text = u"I was in Nebraska for 1 month. I played football for 10 weeks"
        self.assertEquals(process.removePunctuation(text), "I was in Nebraska for 1 month I played football for 10 weeks")

    def test_expand_abbreviation(self):
        text = u"Btw I was in Nebraska for 1 month. I played football for 10 weeks"
        self.assertEquals(process.replaceAbbreviation(text), "by the way i was in nebraska for 1 month. i played football for 10 weeks")

    def test_stemming(self):
        text = ['diagnosed']
        self.assertEquals(process.stemming(text), "diagnos")



if __name__ == '__main__':
    unittest.main()
