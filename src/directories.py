import concurrent.futures
import messages
from directoryfilter import dirs_filter
from lambdafuncs import *
from datetime import datetime as dt


#removes directories in the cache file, does not remove actual copies
def dirs_remove(cache_file, src, directories):    
    try:
        directories = dirs_filter(directories, None)
        dirs_existing = list(map(file_dir_name, cache_file[src].keys()))
        dirs_to_remove = list(set(directories).intersection(set(dirs_existing)))
        dirs_to_remove = [os.path.join(file_path, os.path.basename(src)) for file_path in dirs_to_remove]
        
        for dirs in dirs_to_remove:
            del cache_file[src][dirs]

        messages.dirs_remove_message(dirs_to_remove)
    
        return cache_file
    except KeyError:
        messages.source_not_existing_message_and_exit()     


#prints actual live status of copies, perform no changes, overrides quiet 
def dirs_status(cache_file, src):
    try:
        src_copies = list(cache_file[src].keys())
        
        src_hash, src_build_time, path = file_hash_and_time(src)
        
        print(f'\nOriginal\'s build time: {dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal\'s hash value: {src_hash}', end='\n')
        
        with concurrent.futures.ThreadPoolExecutor() as exc:
            results = exc.map(file_hash_and_time, (copy for copy in src_copies if is_file_exist_and_accessible(copy)))
        
        count = 0

        for hash_and_build in results:
            count += 1
            copy_hash, copy_build_time, path = hash_and_build
            
            diff_hash = ternary_comparision('Equal hash value', 'Unequal hash value', copy_hash, src_hash)

            t_delta = time_elapsed(dt.fromtimestamp(src_build_time) - dt.fromtimestamp(copy_build_time))
            verdict =  ternary_comparision('Update not needed', 'Update recommended', 'Equal hash value', diff_hash)

            
            print(f'\n{count}) {copy_hash[:5]}..{copy_hash[-5:]} {diff_hash}\
                    \n{dt.ctime(dt.fromtimestamp(copy_build_time))} - {str(t_delta)} time elapsed from last update \
                    \n{verdict} for the copy in {file_dir_name(path)}', end='\n')    

        #fix - need to remove unwanted

        # for copy in src_copies:
        #     count += 1
        #     if is_file_exist_and_accessible(copy):
        #         copy_hash, copy_build_time, seed = file_hash_and_time(copy)
        #     else:
        #         print(f'\n{count}) {copy} file path is inaccessible - will be deleted from future updates')
        #         del cache_file[src][copy]
        #         continue
            

        
    except KeyError:
        messages.source_not_existing_message_and_exit()  
    
    return cache_file