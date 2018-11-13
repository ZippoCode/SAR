from google.appengine.ext import ndb


def guestbook_key(id):
    return ndb.Key(Guestbook, id)


class Guestbook(ndb.Model):
    name = ndb.StringProperty()


class Greeting(ndb.Model):
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
