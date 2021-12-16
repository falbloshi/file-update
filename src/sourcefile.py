import os
import shutil
import directoryfilter
import messages
from lambdafuncs import *
from concurrent.futures import ThreadPoolExecutor

#sanity check for source file
def src_get(src):
    if os.path.isfile(src): 
        src_full_path = os.path.realpath(src)
        src_base_name = os.path.basename(src)
    else: 
        messages.source_not_existing_message_and_exit()
    
    return src_full_path, src_base_name


#copies the source in the specified directories, either in added or stored in cache file
def src_copy(directories, src):
    if not messages.args.simulate:
        copy_full = lambda directory: shutil.copy2(src, os.path.normpath(directory))
        ThreadPoolExecutor().map(copy_full, directories) 
        
#adds folders to source path in cache file, copies them if they don't exists
def src_add(cache_file, src, dirs_new=[]):
    try:
        file_hash, file_time = file_hash_and_time(src)[:2]
        BASE = os.path.basename(src)
        dirs_existing = list(map(file_dir_name, cache_file[src].keys()))
        dirs_new = directoryfilter.dirs_existing_filter(dirs_existing, dirs_new)

        for dir_path in dirs_new:
            added_file_path = os.path.join(dir_path, BASE)
            cache_file[src].update({added_file_path: [file_hash, file_time]})     
        
        src_copy(dirs_new, src)
        messages.src_copy_add_message(dirs_new, BASE)
    
    #if source doesn't exist in the json, add it and its folders
    except KeyError or TypeError:
        file_hash, file_time = file_hash_and_time(src)[:2]
        directories = directoryfilter.dirs_filter(dirs_new, None)
        
        if directories:
            cache_file[src] = {}

            for dir_path in directories:
                new_file_path = os.path.join(dir_path, os.path.basename(src))
                cache_file[src].update({new_file_path: [file_hash, file_time]})
            
            src_copy(directories, src)
            messages.src_copy_message(directories, os.path.basename(src))

    return cache_file


#checks the cache file for folders and update them with the newest iteration of the source file
def src_update(cache_file, src):
    file_hash, file_time = file_hash_and_time(src)[:2]
    BASE = os.path.basename(src)
    
    try:
        dirs_existing = directoryfilter.dirs_filter(list(map(file_dir_name, cache_file[src].keys())), "existing")

        for dir_path in dirs_existing:
            updated_file_path = os.path.join(dir_path, BASE)
            cache_file[src].update({updated_file_path: [file_hash, file_time]})     
        
        src_copy(dirs_existing, src)
        messages.src_copy_message(dirs_existing, BASE)
    except KeyError:
        messages.source_not_existing_message_and_exit(src)

    return cache_file

#swaps the source file to whatever is picked, must have the same filename
def src_swap(cache_file, src, swap_file):
    if not is_file_exist_and_accessible(swap_file): messages.source_not_existing_message_and_exit("s")
    
    if os.path.basename(src) == os.path.basename(swap_file):
        try: 
            file_hash, file_time = file_hash_and_time(src)[:2]
            swap_path = os.path.abspath(swap_file)
            success = None

            if is_file_exist_and_accessible(swap_path):
                cache_file.update({swap_path:cache_file[src]})
                cache_file[swap_path].update({src: [file_hash, file_time]})
                
                if cache_file[swap_path][swap_path]: del cache_file[swap_path][swap_path]
                     
                del cache_file[src]
                
                success = True
            
            messages.src_swap_success_message(success, src, swap_path)
            
            return cache_file
        
        except KeyError:
            messages.source_not_existing_message_and_exit()

def src_remove(cache_file, src):
    try:
        del cache_file[src]   
        
        return cache_file

    except KeyError:
        messages.source_not_existing_message_and_exit()
