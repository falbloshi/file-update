from lambdafuncs import *
from datetime import datetime as dt

def dirs_remove(cache, src, directories):    
    if not src: source_not_existing_message_a_exit()
    
    dirs_existing = list(map(file_dir_name , cache[src].getkeys()))
    dirs_to_remove = list(set(directories).intersection(set(dirs_existing)))

    for dir_path in dirs_to_remove:
        removed_file_path = os.path.join(dir_path, src)
        del cache[src][removed_file_path]
    
    return cache

#Prints actual live status of copies, perform no changes, overrides quiet 
def dirs_status(cache, src):
    if not src: source_not_existing_message_a_exit()
 
    src_copies = cache[src].getkeys()
    src_hash, src_build_time = file_hash_a_time(src)
    
    print(f"\nOriginal's build time: {dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal's hash value: {src_hash}", end="\n")
    for copy in src_copies:
        if is_file_exist_a_accessible(copy):
            copy_hash, copy_build_time = file_hash_a_time(copy)
        else:
            print(f"{copy} file path is inaccessable")
            pass
        
        diff_hash = ternary_comparision("Equal hash value", "Unequal hash value", copy_hash, src_hash)
        diff_time = ternary_comparision("Equal build time", "Unequal build time", copy_hash, src_hash)

        t_delta = time_elapsed(dt.fromtimestamp(src_build_time) - dt.fromtimestamp(copy_build_time))
        verdict =  ternary_comparision("Update Not Needed", "Update Recommended", "Equal hash value", diff_hash)

        print(f"{file_dir_name(copy)}:\n {copy_hash[:5]}..{copy_hash[-5:]} {diff_hash}\
                \n{dt.ctime(dt.fromtimestamp(copy_build_time))} - {str(t_delta)} time elapsed from last update \
                \n{verdict} for the copy in {file_dir_name(copy)}", end="\n")    
        
    