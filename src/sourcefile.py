import os
import shutil
from lambdafuncs import *

def src_get(src):
    if os.path.isfile(src): 
        src_full_path = os.path.realpath(src)
        src_base_name = os.path.basename(src)
    else: 
        print(f"{src} is not a valid file")
        exit()
    
    return src_full_path, src_base_name

SRC, CACHE_FILE,SRC_IN_CACHE, DIRS_FILTERED = 0
def src_copy(directories, src, simulate):

    if not simulate:
        for directory in directories:
            shutil.copy2(SRC, os.path.normpath(directory))

def src_update():
    file_hash, file_time = file_hash_a_time(SRC)
    cache_file = CACHE_FILE
    if not SRC_IN_CACHE:
        if DIRS_FILTERED:
            cache_file[SRC] = {}

            for dir_path in DIRS_FILTERED:
                updated_file_path = os.path.join(dir_path, SRC)
                cache_file[SRC].update({updated_file_path: [file_hash, file_time]})

            src_copy(DIRS_FILTERED)
        else:
            if not args.quiet(): 
                print(f"You did not specify directories") 
                args.print_help()                                                            
            exit()

    #updates the folders and add new ones
    else:
        dirs_existing_a_added = dirs_existing_filter(list(cache_file[SRC].getkeys()), DIRS_FILTERED)
        
        if dirs_existing_a_added:
            for dir_path in dirs_existing_a_added:
                updated_file_path = os.path.join(dir_path, SRC)
                cache_file[SRC].update({updated_file_path: [file_hash, file_time]})
            
            src_copy(dirs_existing_a_added)
        else:
            if not args.quiet(): 
                print(f"You did not specify directories or there are empty directories in the records") 
                args.print_help()                                                            
            exit()
    
    return cache_file

def src_swap(swap):
    if not is_file_exist_a_accessible(swap): return
    
    file_hash, file_time = file_hash_a_time(SRC)
    cache_file = CACHE_FILE

def src_remove():
    cache_file = CACHE_FILE
    
    if not SRC_IN_CACHE: source_not_existing_message_a_exit()
    
    del cache_file[SRC]
    
    if not args.quiet:
        print(f"{SRC} removed from cache")
    
    return cache_file
