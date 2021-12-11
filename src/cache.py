import os
import json
import osplatform
import messages

# the src cache file contains key of the source file path
# and each source file path has keys of the copies path
# and each path of copies contains a list, containing a hash value and 
# the last local updated time of the file itself in unix epoch format
# example
# {"source file location": {"copy location 1": [hash_value, date_time], "copy location 2": [hash_value, date_time]}
# "another source file location":  {"copy location 1": [hash_value, date_time], "copy location 2": [hash_value, date_time], "copy location 3": [hash_value, date_time]} }
# here original location 1 has one value, a dictionary, which contains two keys, which are the paths of the copies, and each path has 1 value of list, which contains
# a hash value of the copy and the last update time in unix epoch of the file - these values are actually copies from the source file, rather.
# however when checking the '--status' of the source, it will check each copy individually and compare them, this functionslity is in directories.py as dirs_status()


#gets cache file which stores source file path original location and its copies' locations
#creates empty if does not exist
def src_cache_get():
    src_cache_dir, src_cache_file = osplatform.cache_dir_and_file_get()
    try:
        with open(src_cache_file, 'rb') as jsonfile:
            cache_d = json.load(jsonfile)
            
            return cache_d
          
    except FileNotFoundError:
        messages.src_cache_get_message(src_cache_dir)

        if not os.path.isfile(src_cache_file):
            os.makedirs(src_cache_dir, exist_ok=True)

        with open(src_cache_file, 'x+', encoding='utf-8') as jsonfile:
            empty = {}
            json.dump(empty, jsonfile, indent = 4)
            
            return empty

def src_cache_update(cache_file):
    src_cache_file = osplatform.cache_dir_and_file_get()[1]

    with open(src_cache_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(cache_file, jsonfile, indent = 4)
