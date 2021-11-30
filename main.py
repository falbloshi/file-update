import shutil
import os
import argparse
from datetime import datetime as dt
from hashlib import sha1

DIRS_FILTERED = []
DIRS_REMOVABLE = []

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

    parser.add_argument("-q", "--status", action="store_true",
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

is_same_dirs_as_src = lambda dirs: os.path.normpath(dirs) == os.path.dirname(SRC)
is_dir_exist_a_accessible = lambda dirs: os.path.isdir(dirs) and os.access(dirs, os.R_OK)
is_file_exist_a_accessible = lambda file: os.path.isfile(file) and os.access(file, os.R_OK)
list_item_common_remove = lambda list_a, list_b: list(set(list_a).difference(set(list_b)))
file_dir_name = lambda file: os.path.dirname(file)

#uses the src hash and copy time to the destinion copies 
#for future integrity or update check
def file_hash_a_time(file):
    with open(file, 'rb') as file:
        return sha1(file.read()).hexdigest(), os.path.getmtime(SRC)

def source_not_existing_message():
    if args.quiet: exit()
    else: 
        print("Specified source file does not exist")
        args.print_help()
        exit()

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
import json
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

#remove source file from the history file
def src_remove():
    cache_file = CACHE_FILE
    if SRC_IN_CACHE:
        del cache_file[SRC]
        if not args.quiet:
            print(f"{SRC} removed from cache")
    return cache_file

#remove a copy directory from the history file
DIRS_REMOVABLE = dirs_filter(args.remove)
def dirs_remove():
    if SRC_IN_CACHE:
        cache_file = CACHE_FILE
        dirs_to_remove = list_item_common_remove(DIRS_REMOVABLE, DIRS_FILTERED)
        dirs_existing = list(map(file_dir_name , cache_file[SRC].getkeys()))
        dirs_to_remove = list(set(dirs_to_remove).intersection(set(dirs_existing)))

        for dir_path in dirs_to_remove:
            removed_file_path = os.path.join(dir_path, SRC)
            del cache_file[SRC][removed_file_path]
    else: source_not_existing_message()

    return cache_file

#Prints actual live status of copies, perform no changes, overrides quiet 
def dirs_status():
    cache_file = CACHE_FILE
    if SRC_IN_CACHE:
        src_copies = cache_file[SRC].getkeys()
        src_hash, src_build_time = file_hash_a_time(SRC)
        
        print(f"\nOriginal's build time: {dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal's hash number: {src_hash}", end="\n")
        for copy in src_copies:
            if is_file_exist_a_accessible(copy):
                copy_hash, copy_build_time = file_hash_a_time(copy)
            else:
                print(f"{copy} file path is inaccessable")
                pass
            
            diff_hash = "Equal hash value" if copy_hash == src_hash else "Unequal hash value"
            diff_time = "Equal build time" if copy_build_time == src_build_time else "Unequal build time"      

            if args.verbose:
                src_dt = dt.fromtimestamp(src_build_time)
                copy_dt = dt.fromtimestamp(copy_build_time)
                time_delta = src_dt - copy_dt

                recommendation = "Update Recommended" if copy_hash != src_hash else "Update Not Needed"

                print(f"{file_dir_name(copy)}:\n {copy_hash[:5]}..{copy_hash[-5:]} {diff_hash}\
                            {dt.ctime(dt.fromtimestamp(copy_build_time))} time elapsed from last update {str(time_delta)}")
            
            
            print(f"{file_dir_name(copy)} has {diff_hash} and {diff_time}")

    else: source_not_existing_message()