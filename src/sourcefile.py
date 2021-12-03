import os
import shutil
import directoryfilter
import messages
from lambdafuncs import *

def src_get(src):
    if os.path.isfile(src): 
        src_full_path = os.path.realpath(src)
        src_base_name = os.path.basename(src)
    else: 
        print(f"{src} is not a valid file")
        exit()
    
    return src_full_path, src_base_name


def src_copy(directories, src, simulate):
    if not simulate:
        for directory in directories:
            shutil.copy2(src, os.path.normpath(directory))

def src_update(cache_file, src, directories):
    file_hash, file_time = file_hash_a_time(src)
    #updates the folders and add new ones
    try:
        dirs_existing_a_added = directoryfilter.dirs_existing_filter(list(cache_file[src].getkeys()), directories)
        
        if dirs_existing_a_added:
            for dir_path in dirs_existing_a_added:
                updated_file_path = os.path.join(dir_path, src)
                cache_file[src].update({updated_file_path: [file_hash, file_time]})
            
            src_copy(dirs_existing_a_added)   
    except KeyError:
        if directories:
            cache_file[src] = {}

            for dir_path in directories:
                updated_file_path = os.path.join(dir_path, src)
                cache_file[src].update({updated_file_path: [file_hash, file_time]})

            src_copy(directories)
    return cache_file

def src_swap(cache_file, src, swap_file):
    if not is_file_exist_a_accessible(swap_file): return
    try: 
        bool(cache_file[src])
        file_hash, file_time = file_hash_a_time(src)

        cache_file.update({swap_file:cache_file[src]})
        cache_file[swap_file].update({src: [file_hash, file_time]})

        del cache_file[src]

        return cache_file
    except KeyError:
        messages.source_not_existing_message_a_exit()

def src_remove(cache_file, src):
    try:
        del cache_file[src]   
        return cache_file

    except KeyError:
        messages.source_not_existing_message_a_exit()