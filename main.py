import shutil
import os
import argparse

DIRS_FILTERED = []
ADD_FILTERED = []

def command_parser():
    parser = argparse.ArgumentParser(
            description = 'Updates multiple copies of a file(SRC) residing in different directories(DIRS)')

    parser.add_argument("source", type=str, metavar="SRC",
                        help="the original file")

    parser.add_argument("-d","--dirs", metavar="DIRS", type=str, nargs='+', required=True,
                        help="directory of the copies")

    parser.add_argument("-a", "--add", metavar="DIRS", type=str, nargs='+',
                        help="adds a folder to an existing source file")

    parser.add_argument("-u", "--update", action="store_true",
                        help="update existing source file")

    parser.add_argument("-p", "--path", action="store_true",
                        help="displays the absolute path of the source file")

    parser.add_argument("-s", "--simulate", action="store_true",
                        help="simulate copy process, don't perform real changes")

    parser.add_argument("-q", "--quiet", action="store_true",
                        help="display no output")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="display more information in output")

    args = parser.parse_args()
    return args
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

if args.path and os.path.isfile(args.source):
        print(f"the fullpath name of {BASE} is {SRC}")

#removing non directory listing to process reachable and unreachable paths
def dirs_filter():
    
    dirs = set([dirs for dirs in args.dirs if os.path.isdir(dirs)\
            and os.access(dirs, os.R_OK)\
            and not is_same_dirs_as_src(dirs)])
  
    if args.verbose:
        num = 1
        
        for item in list(set(args.dirs)-dirs):
            if is_same_dirs_as_src(item): 
                print(f"{num} - \"{item}\" removed - cannot copy to the same directory as the source file")
            elif os.path.isdir(item): 
                print(f"{num} - \"{item}\" removed - could be missing file mount or user access")
            elif os.path.isabs(item): 
                print(f"{num} - \"{item}\" removed - could be missing file mount or invalid directory")
            else: 
                print(f"{num} - \"{item}\" removed - not a directory")
            num += 1
    elif args.quiet: pass
    else: 
        if args.dirs != dirs: print("Invalid directories removed")

    return list(dirs)
DIRS_FILTERED = dirs_filter()

def add_filter():
    history_file, src_not_in_jfile = src_exists()
    dirs = []
    if not src_not_in_jfile:
        directory_in_hist = [os.path.dirname(dirs) for dirs in list(history_file[SRC].getkeys()]
        dirs = set([dirs for dirs in args.add if os.path.isdir(dirs)\
                and os.access(dirs, os.R_OK)\
                and not is_same_dirs_as_src(dirs)\
                and dirs not in directory_in_hist])
    return list(dirs)
ADD_FILTERED = add_filter()
DIRS_FILTERED += ADD_FILTERED

#copy file to specified folders in --dirs and --add key arguments
def src_copy():
    if not args.simulate:
        for directory in DIRS_FILTERED:
            shutil.copy2(SRC, os.path.normpath(directory))

    if args.verbose:
        print(f"\nCopying {BASE} in ")
        num = 1
        for item in DIRS_FILTERED:
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

#uses the src hash and copy time to the destinion copies 
#for future integrity or update check
from hashlib import sha1
from time import ctime
def src_file_hash_time(file):
    with open(file, 'rb') as file:
        return sha1(file.read()).hexdigest(), ctime()

def src_exists():
    history_file  = src_history_jfile_get()
    not_in_jfile = SRC not in history_file

    return  history_file, not_in_jfile

#if src does not exist in source_history.json, 
#try to create new src and dir list and add to the json file
#if src exists in source_history.json, 
#try to update existing folders and or add new ones if added through -a flag
def src_update():
    history_file, not_in_jfile  = src_exists()

    if not_in_jfile:
        history_file[SRC] = {} 
    
    file_hash, file_time = src_file_hash_time(SRC)

    #adds the folders
    if not_in_jfile:
        for dir_path in DIRS_FILTERED:
            file_path = os.path.join(dir_path, SRC)
            history_file[SRC].update({file_path: [file_hash, file_time]})
    #updates the folders and add new if flagged
    else:
        dirs_existing = list(history_file[SRC].getkeys())
        dirs_existing_and_added = ADD_FILTERED + dirs_existing
        
        for dir_path in dirs_existing_and_added :
            file_path = os.path.join(dir_path, SRC)
            history_file[SRC].update({file_path: [file_hash, file_time]})
    
    src_copy()
    
    return history_file