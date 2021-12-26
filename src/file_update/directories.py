from . import messages
from . import lambdas
from . import hashfile
from .directoryfilter import dirs_filter
from .osplatform import windows_drive_letter_resolve as wdlr, IS_WINDOWS
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor
import os.path

verbose = messages.args.verbose

def dirs_remove(cache_file, src, directories):
    """
    Removes directories in the cache file, 
    does not remove actual copies
    """
    
    try:
        directories = dirs_filter(directories, None)
        
        dirs_existing = list(map(lambdas.file_dir_name, cache_file[src].keys()))
        
        dirs_to_remove = list(set(directories).intersection(set(dirs_existing)))
        
        dirs_to_remove = [os.path.join(file_path, os.path.basename(src)) for file_path in dirs_to_remove]
    
        for dirs in dirs_to_remove:
            del cache_file[src][dirs]

        messages.dirs_remove_message(dirs_to_remove)
    
        return cache_file
    
    except KeyError:
        messages.src_not_existing_message_and_exit()     


def dirs_status(cache_file, src):
    """
    Prints actual live status of copies, 
    perform no changes, overrides quiet
    """

    try:
        src_copies = list(set(cache_file[src].keys()))
        
        src_hash, src_build_time, path = hashfile.file_hash_and_time(src)
        
        print(f'\nOriginal\'s build time: {dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal\'s hash value: {src_hash}', end='\n')
        
        
        count = 0
        for copy in src_copies.copy():
            if lambdas.is_file_exist_and_accessible(copy): continue
            else:
                if IS_WINDOWS:
                    for path in wdlr(copy):
                        if lambdas.is_file_exist_and_accessible(path):
                            
                            src_copies.insert(path, src_copies.index(copy))
                            
                            src_copies.remove(copy)
                            
                            cache_file[src].update({path: cache_file[src][copy]})
                            
                            print(f'for "{copy}"\t drive letter resolved to {path[:1]}')
                            
                            break
                
                count += 1
                
                print(f'\n{count}) {copy.center(80, "*")}\n' + 'folder does not exists or inaccessible, will be removed from future updates'.center(80, "*"))
                
                src_copies.remove(copy)
                
                del cache_file[src][copy]

            
        results = ThreadPoolExecutor().map(hashfile.file_hash_and_time, src_copies)
        count = 0

        for hash_and_build in results:
            count += 1
            
            copy_hash, copy_build_time, path = hash_and_build
            
            diff_hash = lambdas.ternary_comparision('Equal hash value', 'Unequal hash value', copy_hash, src_hash)
            
            t_delta = lambdas.time_elapsed(dt.fromtimestamp(src_build_time) - dt.fromtimestamp(copy_build_time))
            
            verdict =  lambdas.ternary_comparision('Update not needed', 'Update recommended', 'Equal hash value', diff_hash)

            if not verbose:
                copy_hash = f'{copy_hash[:5]}..{copy_hash[-5:]}'

            print(f'\n{count}) {copy_hash} {diff_hash}\
                    \n{dt.ctime(dt.fromtimestamp(copy_build_time))} - {str(t_delta)} time elapsed from last update \
                    \n{verdict} for the copy in {lambdas.file_dir_name(path)}', end='\n')    
        
    except KeyError:
        messages.src_not_existing_message_and_exit()  
    
    return cache_file