import os
import json
import osplatform
import messages

def src_cache_get():
    src_cache_dir, src_cache_file = osplatform.cache_dir_a_file_get()
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
    src_cache_file = osplatform.cache_dir_a_file_get()[1]

    with open(src_cache_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(cache_file, jsonfile, indent = 4)
