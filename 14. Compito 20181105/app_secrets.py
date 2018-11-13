import os
import hashlib

app_secret_key = hashlib.sha1(os.urandom(128)).hexdigest()
music_key = "fc3daef925fffa01feb02f41436017d3"
