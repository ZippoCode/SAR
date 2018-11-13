import os
import hashlib

app_secret_key = hashlib.sha1(os.urandom(128)).hexdigest()
mashape_key = "KEY-MASHAPE"