import shutil
import os
import argparse


def command_parser():
    parser = argparse.ArgumentParser(
            description = 'Updates multiple copies of a file(SRC) residing in different directories(DIRS)')

    parser.add_argument("source", type=str, metavar="SRC",
                        help="the original file")

    parser.add_argument("-d","--dirs", metavar="DIRS", type=str, nargs='+', required=True,
                        help="directory of the copies")

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
    
    dirs = [dirs for dirs in args.dirs if os.path.isdir(dirs)\
            and os.access(dirs, os.R_OK)\
            and not is_same_dirs_as_src(dirs)]
  
    if args.verbose:
        num = 1
        
        for item in list(set(args.dirs)-set(dirs)):
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

    return dirs
DIRS_FILTERED = dirs_filter()

#copy file to specified folders
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
    
    return DIRS_FILTERED

### Json ###
import json

#returns source_history.json if exists, else creates new one
def src_jfile_get():
    #stackoverflow.com/a/35249327
    src_hist_dir = os.path.expanduser("~") + ".config/fupdate"
    src_hist_file = src_hist_dir + "/source_history.json"
    try:
        with open(src_hist_file, 'r', encoding='utf-8') as j_file:	
            source_history = json.load(j_file)
            return source_history
		
    except FileNotFoundError: 
        #stackoverflow.com/a/35249327
        if not os.path.isfile(src_hist_file):
            os.makedirs(src_hist_dir, exist_ok=True)
        
        if not args.quiet:
            print(f'History file did not exist. Creating source_history.json in {src_hist_dir}')
            
        with open(src_hist_file, 'x+', encoding='utf-8') as j_file:
            empty = {}
            json.dump(empty, j_file, indent = 4)
            return src_jfile_get()
            


from hashlib import sha1
def dirs_file_hash(file):
    with open(file, 'rb') as file:
        return sha1(file.read()).hexdigest

#if src does not exist in source_history.json, 
#try to create new src and dir list and add to the json file
def src_create():
    source_file  = src_jfile_get()
   
    for dir_path in DIRS_FILTERED:
        file_path = os.path.join(dir_path, SRC)
        
        if os.path.isfile(file_path):
            file_hash = dirs_file_hash(file_path)
        
    source_file.update(SRC=[file_hash, ])  
    pass

#if src exists in source_history.json, 
#try to update existing folders and or add new ones if added through -a flag
def src_update(src):
    pass