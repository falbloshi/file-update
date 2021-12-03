import os
import json 
import osplatform

def src_cache_get():

    src_cache_file, src_cache_dir = osplatform.cache_dir_a_file()
    try:
        with open(src_cache_file, 'r', encoding='utf-8') as j_file:	
            source_history = json.load(j_file)
            return source_history
	
    except FileNotFoundError: 
        if not os.path.isfile(src_cache_file):
            os.makedirs(src_cache_dir, exist_ok=True)
                    
        with open(src_cache_file, 'x+', encoding='utf-8') as j_file:
            empty = {}
            json.dump(empty, j_file, indent = 4)
            
            return src_cache_get()

def src_cache_update(cache_file):
    src_cache_file = osplatform.cache_dir_a_file()[0]

    with open(src_cache_file, 'w', encoding='utf-8') as j_file:
            json.dump(cache_file, j_file, indent = 4)