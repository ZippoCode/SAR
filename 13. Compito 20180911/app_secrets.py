import os
import hashlib

app_secret_key = hashlib.sha1(os.urandom(128)).hexdigest()
api_key = "2138c6f4"
