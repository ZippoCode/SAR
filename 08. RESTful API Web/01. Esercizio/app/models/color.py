from google.appengine.ext import ndb


class Color(ndb.Model):
    label = ndb.StringProperty(required=True, indexed=True)
    red = ndb.IntegerProperty(required=True)
    green = ndb.IntegerProperty(required=True)
    blue = ndb.IntegerProperty(required=True)

def create_color(name, red, green, blue):
    color = Color(id=name)
    color.label = name
    color.red = red
    color.green = green
    color.blue = blue
    return color
