from datetime import datetime

from google.appengine.ext import ndb


class StringWord(ndb.StringProperty):

    def _to_base_type(self, value):
        return str(value).strip().title()


class StringPhrase(ndb.StringProperty):

    def _to_base_type(self, value):
        value = str(value)
        return "%s%s" % (value[0].upper(), value[1:].lower())


class DataCreated(ndb.DateTimeProperty):

    def _from_base_type(self, value):
        data = datetime.strftime(value, "%Y-%m-%d %H:%M:%S")
        return data


class Frequent(ndb.Model):
    error = StringWord(indexed=True)
    list_suggestion = StringWord(repeated=True)
    counter = ndb.IntegerProperty(indexed=True, default=1)
    created = DataCreated(indexed=True, auto_now_add=True)


class Phrase(ndb.Model):
    original = StringPhrase(indexed=True)
    suggestion = StringPhrase(indexed=True)
    counter = ndb.IntegerProperty(default=1)
    created = DataCreated(auto_now_add=True)


class Word(ndb.Model):
    correct = StringWord(indexed=True)
    errors = StringWord(repeated=True)
    counter = ndb.IntegerProperty(indexed=True, default=1)
