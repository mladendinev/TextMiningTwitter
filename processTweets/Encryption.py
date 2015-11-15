import base64
from Crypto.Cipher import AES
from Crypto import Random
import os
class EncryptData():

    def __init__(self):
        self._configFile = "/home/mladen/FinalYearProject/configFiles/key.py"
        self._config = {}
        execfile(self._configFile, self._config)
        self.BS = 16
        self._pad = lambda s: s + ( self.BS - len(s) %  self.BS) * chr( self.BS - len(s) %  self.BS)
        self._unpad = lambda s : s[:-ord(s[len(s)-1:])]
        self._key = self._config["key"]

    def encrypt(self,text):
        raw = self._pad(text)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._key,AES.MODE_CBC,iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    #     print self.key

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt( enc[16:] ))