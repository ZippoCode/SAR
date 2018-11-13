import base64

from google.appengine.ext import ndb


class EncodeString(ndb.StringProperty):

    def _to_base_type(self, stringa):
        return base64.urlsafe_b64encode(stringa.encode('UTF-8'))


class Sondaggio(ndb.Model):
    encode = EncodeString(indexed=True)
    title = ndb.StringProperty(indexed=True)
    positivi = ndb.IntegerProperty(indexed=True, default=0)
    negativi = ndb.IntegerProperty(indexed=True, default=0)
    astenuti = ndb.IntegerProperty(indexed=True, default=0)
