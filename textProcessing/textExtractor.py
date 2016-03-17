__author__ = 'mladen'


def getTerms(fileName):
    # os.path.join('/home/mladen/TextMiningTwitter/word_lists',       )
    try:
        with open(fileName, 'r') as disorderFile:
            terms=[]
            disorderList = disorderFile.readlines()
            for line in disorderList:
                line = line.lower()
                line = line.rstrip('\n')
                terms.append(line)
            return terms
    except Exception as e:
        print "Failed to read disorders from file because:", e
        raise SystemExit


def getAbbreviations():
    filename = "/home/mladen/TextMiningTwitter/word_lists/abbreviations.txt"
    dictionary = {}
    with open(filename) as f:
        for line in f.readlines():
            line = line.lower()
            abbreviation = line.split(None, 1)[0]
            # print word
            replacement = line.replace("\n", "").split(None, 1)[1]
            dictionary.update({abbreviation: replacement})
        return dictionary
