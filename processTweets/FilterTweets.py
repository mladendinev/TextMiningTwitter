__author__ = 'mladen'
from database import dbOperations
from Encryption import EncryptData


class FilterTweets():

    def __init__(self):
        self.dbOps = dbOperations

    def filterTweetsFromDatabase(self):
        tweets = self.dbOps.dbOperations().returnFilteredTweets("diagnosticTweets")


if __name__ == '__main__':
    print "Searching tweets..."
    enc = EncryptData().encrypt("2312312")
    saveJson = {'encrypt' : enc}
    dbOperations.dbOperations().insertData(saveJson, "testEncrypt")
    decryptText = dbOperations.dbOperations().returnAllTweetsFromCollection("testEncrypt")
    text =  EncryptData().decrypt(decryptText["encrypt"])
    print text
    # print enc