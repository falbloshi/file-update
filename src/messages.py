from lambdafuncs import *

def dirs_filter_message(verbosity, list):
    if verbosity:
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
    elif verbosity: pass
    else: 
        if directory != dirs: print("Invalid directories removed")

def dirs_filter_existing_message(verbosity):
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
    
def src_copy_message(verbosity):
    if args.verbose:
            print(f"\nCopying {BASE} in ")
            num = 1
            for item in directories:
                print(f"{num} - {os.path.normpath(item)}")
                num += 1
        elif args.quiet: pass
        else: print(f"File {BASE}, Copied Sucessfuly")
    
def source_not_existing_message_a_exit(help_message):
    if args.quiet: exit()
    else: 
        print("Specified source file does not exist")
        args.print_help()
        exit()
def  scr_jfile_get_messages():
    if not args.quiet:
        print(f'History file did not exist. Creating source_history.json in {src_cache_dir}')