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
        messages.source_not_existing_message_a_exit()
    
    return src_full_path, src_base_name


def src_copy(directories, src):
    if not messages.args.simulate:
        for directory in directories:
            shutil.copy2(src, os.path.normpath(directory))

def src_update(cache_file, src, new_directories=[]):
    file_hash, file_time = file_hash_a_time(src)
    #updates the folders and add new ones
    try:
        bool(cache_file[src]) #sanity check
        print("We are in the existing after cache_file check")
        dirs_existing_a_added = directoryfilter.dirs_existing_filter(list(map(file_dir_name, cache_file[src].keys())), new_directories)
    
        for dir_path in dirs_existing_a_added:
            updated_file_path = os.path.join(dir_path, os.path.basename(src))
            cache_file[src].update({updated_file_path: [file_hash, file_time]})     
        
        src_copy(dirs_existing_a_added, src)
        messages.src_copy_message(dirs_existing_a_added, os.path.basename(src))
    #if src doesn't exist in json, add it and its folders
    except KeyError or TypeError:
        print("We are in the New strict")
        directories = directoryfilter.dirs_filter(new_directories)
        if directories:
            cache_file[src] = {}

            for dir_path in directories:
                updated_file_path = os.path.join(dir_path, os.path.basename(src))
                cache_file[src].update({updated_file_path: [file_hash, file_time]})
            
            src_copy(directories, src)
            messages.src_copy_message(directories, os.path.basename(src))
        
    return cache_file

def src_swap(cache_file, src, swap_file):
    if not is_file_exist_a_accessible(swap_file): messages.source_not_existing_message_a_exit(swap_file)
    if os.path.basename(src) == os.path.basename(swap_file):
        try: 
            file_hash, file_time = file_hash_a_time(src)

            cache_file.update({swap_file:cache_file[src]})
            cache_file[swap_file].update({src: [file_hash, file_time]})

            del cache_file[src]

            return cache_file
        except KeyError:
            messages.source_not_existing_message_a_exit()
    else:
        pass

def src_remove(cache_file, src):
    try:
        del cache_file[src]   
        return cache_file

    except KeyError:
        messages.source_not_existing_message_a_exit()