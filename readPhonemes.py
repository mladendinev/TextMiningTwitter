__author__ = 'mladen'
import collections

def lookforwords(searchWord):

    dictionary = {}
    with open('beep.txt') as f:
        for i in xrange(11):
            f.next()
        for line in f:
            # print
            line = line.lower()
            word = line.split(None, 1)[0]
            # print word
            phonemes = line.replace("\n", "").split(None, 1)[1]
            if word.startswith("\\") | word.startswith("\\"):
                pass
            else:
                dictionary.update({word: phonemes})

        phonemes = {}
        find = searchWord.split()
        for each in find:
            if dictionary.has_key(each):
                phonemes.update({each:dictionary.get(each)})
            else :
                print "No phoneme found for ", each
                return
        return phonemes

if __name__ == "__main__":
    word = raw_input("Please enter words: ")
    dictionary = lookforwords(word)
    # ordered = collections.OrderedDict(sorted(dictionary.items()))
    print dictionary