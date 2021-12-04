from commandparse import args 
from lambdafuncs import *

def dirs_filter_message(list_a, list_b):
    if args.verbose:
        num = 1
        for item in list_item_common_remove(set(list_a), set(list_b)):
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
        if list_a != list_b: print("Invalid directories removed")

def dirs_existing_filter_message(directory, filtered_directory, new_directory_list):
    if args.verbose:
        num = 1    
        for item in directory:
            if item in new_directory_list: 
                print(f"{num} - \"{item}\" removed - already exists")
                num += 1
            elif item not in filtered_directory: 
                print(f"{num} - \"{item}\" removed - folder does not exist or inaccessible")
                num += 1
            
    elif args.quiet: pass
    else: 
        if directory != filtered_directory: print("Invalid directories removed")

def dirs_remove_message(dirs_to_remove):
    if args.verbose:
        num = 1
        for each in list(dirs_to_remove):
            print(f"{num} - \"{each}\" removed from from source")
    elif args.quiet: pass
    else: 
        print(f"Directories removed from update")



def source_not_existing_message_a_exit(swap=''):
    if args.quiet: exit()
    else: 
        file_type = "source" if args.swap else "swap"
        print(f"Specified {file_type} file does not exist")
        args.print_help()
        exit()

def src_copy_add_message(directories, src_name):
    if args.verbose:
            print(f"\nFolders added {src_name} successfuly ")
            num = 1
            for item in directories:
                print(f"{num} - {os.path.normpath(item)}")
                num += 1
    elif args.quiet: pass
    else: print(f"File {src_name}, added sucessfuly")


def src_copy_message(directories, src_name, copy_or_updating="copying"):

    if args.verbose:
            print(f"\nCopying {src_name} in ")
            num = 1
            for item in directories:
                print(f"{num} - {os.path.normpath(item)}")
                num += 1
    elif args.quiet: pass
    else: print(f"File {src_name}, copied sucessfuly")
    
def  src_cache_get_message(src_cache_dir):
    if not args.quiet:
        print(f'Cache file did not exist. Creating cache.json in {src_cache_dir}')