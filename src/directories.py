import messages
from directoryfilter import dirs_filter
from lambdafuncs import *
from datetime import datetime as dt


def dirs_remove(cache_file, src, directories):    
    try:
        directories = dirs_filter(directories)
        dirs_existing = list(map(file_dir_name, cache_file[src].keys()))
        dirs_to_remove = list(set(directories).intersection(set(dirs_existing)))

        dirs_to_remove = [os.path.join(file_path, os.path.basename(src)) for file_path in dirs_to_remove]
        for dirs in dirs_to_remove:
            del cache_file[src][dirs]

        messages.dirs_remove_message(dirs_to_remove)
    
        return cache_file
    except KeyError:
        messages.source_not_existing_message_a_exit()     


#Prints actual live status of copies, perform no changes, overrides quiet 
def dirs_status(cache_file, src):
    try:
        src_copies = cache_file[src].keys()
        src_hash, src_build_time = file_hash_a_time(src)
        
        print(f"\nOriginal's build time: {dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal's hash value: {src_hash}", end="\n")
        for copy in src_copies:
            if is_file_exist_a_accessible(copy):
                copy_hash, copy_build_time = file_hash_a_time(copy)
            else:
                print(f"{copy} file path is inaccessible")
                pass
            
            diff_hash = ternary_comparision("Equal hash value", "Unequal hash value", copy_hash, src_hash)

            t_delta = time_elapsed(dt.fromtimestamp(src_build_time) - dt.fromtimestamp(copy_build_time))
            verdict =  ternary_comparision("Update not needed", "Update recommended", "Equal hash value", diff_hash)

            print(f"\n{file_dir_name(copy)}:\n{copy_hash[:5]}..{copy_hash[-5:]} {diff_hash}\
                    \n{dt.ctime(dt.fromtimestamp(copy_build_time))} - {str(t_delta)} time elapsed from last update \
                    \n{verdict} for the copy in {os.path.basename(copy)}", end="\n")    
    except KeyError:
        messages.source_not_existing_message_a_exit()  
    