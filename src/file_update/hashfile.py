import os.path
from hashlib import sha1

def file_hash_and_time(file):
    """
    returns a file's hash value and time of last update
    """
    with open(file, 'rb') as openfile:
        return sha1(openfile.read()).hexdigest(), os.path.getmtime(file), file