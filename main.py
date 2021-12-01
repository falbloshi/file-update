import shutil
import os
import argparse
import datetime
import json
from datetime import datetime as dt, timedelta
from hashlib import sha1

DIRS_FILTERED = []
DIRS_REMOVABLE = []

##lambda functions
is_same_dirs_as_src = lambda dirs: os.path.normpath(dirs) == os.path.dirname(SRC)
is_dir_exist_a_accessible = lambda dirs: os.path.isdir(dirs) and os.access(dirs, os.R_OK)
is_file_exist_a_accessible = lambda file: os.path.isfile(file) and os.access(file, os.R_OK)
list_item_common_remove = lambda list_a, list_b: list(set(list_a).difference(set(list_b)))
file_dir_name = lambda file: os.path.dirname(file)
time_elapsed = lambda t_delta: datetime.timedelta(seconds=t_delta.seconds, days=t_delta.days)
ternary_comparision = lambda message_true, message_false, object_1, object_2: message_true if object_1 == object_2 else message_false
##lambda functions

##regular functions
#-uses the src hash and copy time to the destinion copies in json file
#-also for future integrity or update check of copies
def file_hash_a_time(file):
    with open(file, 'rb') as file:
        return sha1(file.read()).hexdigest(), os.path.getmtime(SRC)

def source_not_existing_message_a_exit():
    if args.quiet: exit()
    else: 
        print("Specified source file does not exist")
        args.print_help()
        exit()
##regular functions

def command_parser():
    parser = argparse.ArgumentParser(
            description = 'Updates multiple copies of a file(SRC) residing in different directories(DIRS)')

    parser.add_argument("source", type=str, metavar="SRC",
                        help="SRC, the origin source file to be copied")

    parser.add_argument("-a", "--add", metavar="DIRS", type=str, nargs='+',
                        help="adds directories to copy an existing SRC file")

    parser.add_argument("-u", "--update", action="store_true",
                        help="update existing SRC file")

    parser.add_argument("-s", "--simulate", action="store_true",
                        help="simulate copy process, don't perform real changes")

    parser.add_argument("--status", action="store_true",
                        help="prints live status of a SRC file and its related copies; overrides -q flag")
    
    parser.add_argument("--swap", metavar="SWP", action="store_true", type=str, nargs="?",
                        help="prints live status of a SRC file and its related copies; overrides -q flag")

    parser.add_argument("-q", "--quiet", action="store_true",
                        help="display no output")

    parser.add_argument("-d", "--delete", metavar="SRC", action="store_true",
                        help="deletes an origin file(SRC) from history, will not delete the real file")
    
    parser.add_argument("-r", "--remove", metavar="DIRS", action="store_true", type=str, nargs='+',
                        help="removes a copy's directory(DIRS) from history from the specified SRC, will not delete the real directory")                   

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="display more information in output")


    return parser.parse_args()
args = command_parser()

#checks if source is a file in current working directory or an absolute path
def src_get():
    if os.path.isfile(args.source): 
        src_full_path = os.path.realpath(args.source)
        src_base_name = os.path.basename(args.source)
    else: 
        print(f"{args.source} is not a valid file")
        args.print_help()
        exit()
    
    return src_full_path, src_base_name
SRC, BASE = src_get()


#removing non directory listing to process reachable and unreachable paths
def dirs_filter(directory):
    dirs = set([dirs for dirs in directory \
            if is_dir_exist_a_accessible(dirs)
            and not is_same_dirs_as_src(dirs)])
  
    if args.verbose:
        num = 1
        
        for item in list_item_common_remove(set(directory), dirs):
            if is_same_dirs_as_src(item): 
                print(f"{num} - \"{item}\" removed - no action to the same directory as the source file")
            elif os.path.isdir(item): 
                print(f"{num} - \"{item}\" removed - could be missing file mount or user access")
            elif os.path.isabs(item): 
                print(f"{num} - \"{item}\" removed - could be missing file mount or invalid directory")
            else: 
                print(f"{num} - \"{item}\" removed - not a directory")
            num += 1
    elif args.quiet: pass
    else: 
        if directory != dirs: print("Invalid directories removed")

    return list(dirs)
DIRS_FILTERED = dirs_filter(args.add)

def dirs_existing_filter(directory, new_directory_list=[]):
    #assuming they are keys in cache file 
    directory = [os.path.dirname(dirs) for dirs in directory]

    filtered_directory = [dirs for dirs in directory \
                            if is_dir_exist_a_accessible(dirs)\
                            and dirs not in new_directory_list]
    if args.verbose:
        num = 1    
        for item in directory:
            if item not in filtered_directory: 
                print(f"{num} - \"{item}\" removed - folder does not exist or inaccessible")
            elif item in new_directory_list: 
                print(f"{num} - \"{item}\" removed - already exists")
            num += 1
    elif args.quiet: pass
    else: 
        if directory != filtered_directory: print("Invalid directories removed")

    return filtered_directory + new_directory_list

#copy file to specified folders in --add key arguments
def src_copy(directories):
    if not args.simulate:
        for directory in directories:
            shutil.copy2(SRC, os.path.normpath(directory))

    if args.verbose:
        print(f"\nCopying {BASE} in ")
        num = 1
        for item in directories:
            print(f"{num} - {os.path.normpath(item)}")
            num += 1
    elif args.quiet: pass
    else: print(f"File {BASE}, Copied Sucessfuly")

### Json ###
#returns source_history.json if exists, else creates new one
def src_history_jfile_get():
    #stackoverflow.com/a/35249327
    src_hist_dir = os.path.expanduser("~") + ".config/fupdate"
    src_hist_file = src_hist_dir + "/source_history.json"
    try:
        with open(src_hist_file, 'r', encoding='utf-8') as j_file:	
            source_history = json.load(j_file)
            return source_history
	
    except FileNotFoundError: 
        #stackoverflow.com/a/35249327, if you don't copy from sof, what use of you?
        if not os.path.isfile(src_hist_file):
            os.makedirs(src_hist_dir, exist_ok=True)
        
        if not args.quiet:
            print(f'History file did not exist. Creating source_history.json in {src_hist_dir}')
            
        with open(src_hist_file, 'x+', encoding='utf-8') as j_file:
            empty = {}
            json.dump(empty, j_file, indent = 4)
            
            return src_history_jfile_get()
CACHE_FILE  = src_history_jfile_get()
SRC_IN_CACHE = SRC in CACHE_FILE 



#if src does not exist in source_history.json, 
#try to create new src and dir list and add to the json file
#if src exists in source_history.json, 
#try to update existing folders and or add new ones if added through -a flag
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

#swap source to a new folder, and add the old source to the cache file
def src_swap():
    if not SRC_IN_CACHE: source_not_existing_message_a_exit()
    if not is_file_exist_a_accessible(args.swap): return
    
    file_hash, file_time = file_hash_a_time(SRC)
    cache_file = CACHE_FILE
    
#remove source file from the history file
def src_remove():
    cache_file = CACHE_FILE
    
    if not SRC_IN_CACHE: source_not_existing_message_a_exit()
    
    del cache_file[SRC]
    
    if not args.quiet:
        print(f"{SRC} removed from cache")
    
    return cache_file

#remove a copy directory from the history file
DIRS_REMOVABLE = dirs_filter(args.remove)
def dirs_remove():
    cache_file = CACHE_FILE
    
    if not SRC_IN_CACHE: source_not_existing_message_a_exit()
    
    dirs_to_remove = list_item_common_remove(DIRS_REMOVABLE, DIRS_FILTERED)
    dirs_existing = list(map(file_dir_name , cache_file[SRC].getkeys()))
    dirs_to_remove = list(set(dirs_to_remove).intersection(set(dirs_existing)))

    for dir_path in dirs_to_remove:
        removed_file_path = os.path.join(dir_path, SRC)
        del cache_file[SRC][removed_file_path]
    
    return cache_file

#Prints actual live status of copies, perform no changes, overrides quiet 
def dirs_status():
    if not SRC_IN_CACHE: source_not_existing_message_a_exit()

    cache_file = CACHE_FILE
    src_copies = cache_file[SRC].getkeys()
    src_hash, src_build_time = file_hash_a_time(SRC)
    
    print(f"\nOriginal's build time: {dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal's hash value: {src_hash}", end="\n")
    for copy in src_copies:
        if is_file_exist_a_accessible(copy):
            copy_hash, copy_build_time = file_hash_a_time(copy)
        else:
            print(f"{copy} file path is inaccessable")
            pass
        
        diff_hash = ternary_comparision("Equal hash value", "Unequal hash value", copy_hash, src_hash)
        diff_time = ternary_comparision("Equal build time", "Unequal build time", copy_hash, src_hash)

        if args.verbose:
            t_delta = time_elapsed(dt.fromtimestamp(src_build_time) - dt.fromtimestamp(copy_build_time))
            verdict =  ternary_comparision("Update Not Needed", "Update Recommended", "Equal hash value", diff_hash)

            print(f"{file_dir_name(copy)}:\n {copy_hash[:5]}..{copy_hash[-5:]} {diff_hash}\
                    \n{dt.ctime(dt.fromtimestamp(copy_build_time))} - {str(t_delta)} time elapsed from last update \
                    \n{verdict} for the copy in {file_dir_name(copy)}", end="\n")    
        
        print(f"{file_dir_name(copy)} has {diff_hash} and {diff_time} - {verdict}", end="\n")
    


