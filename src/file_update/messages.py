from .commandparse import args
from . import lambdas
import os.path

num_global = 0


def dirs_filter_message(directories, filtered_directories, message):

    global num_global
    
    removed = lambdas.list_item_common_remove(
        set(directories), set(filtered_directories))
    
    if args.verbose:
        if message and removed: print(f'Verifying {message}:')
        
        for num, dirs in enumerate(removed, 1):
            if lambdas.is_same_dirs_as_src(dirs, args.source): 
                print(f'{num}) - \'{dirs}\' removed - no action to the same \
directory as the source file')
            elif os.path.isdir(dirs): 
                print(f'{num}) - \'{dirs}\' removed - could be missing file \
mount or user access')
            elif os.path.isabs(dirs): 
                print(f'{num}) - \'{dirs}\' removed - could be missing file \
mount or invalid directory')
            else: 
                print(f'{num}) - \'{dirs}\' removed - not a directory')
            num_global = num
    elif args.quiet: 
        return None
    else:  
        if removed:
            diff = len(removed)
            one = diff == 1
            print(f'{"One" if one else f"Nos. {diff} of"} invalid \
director{"y" if one else "ies"} removed')


def dirs_new_filter_message(existing_directories, filtered_new_directories):
   
    ints = (
        set(existing_directories).intersection(set(filtered_new_directories)))
    
    if args.verbose:
        ms = 'removed - already exists in cache'
        print('\n'.join((f'{num + num_global}) - \'{dirs}\' {ms}'
                        for num, dirs in enumerate(ints, 1))))
    elif args.quiet: 
        return None
    else: 
        if ints:
            ms = f'{"One" if len(ints) == 1 else f"Nos. {len(ints)} of"}'
            print(f'{ms} director{"y" if len(ints) == 1 else "ies"} already \
exists in cache')


def dirs_remove_message(dirs_to_remove):

    if args.quiet: 
        return None
    elif not dirs_to_remove:
        print('No directories to remove')
    elif args.verbose:
        ms = 'removed from cache file'
        print('\n'.join((f'{num + num_global}) - "{dirs}" - {ms}' 
                        for num, dirs in enumerate(dirs_to_remove, 1))))
    else: 
        print(f'Director{"y" if len(dirs_to_remove) == 1 else "ies"} \
removed from future updates')


def src_not_existing_message_and_exit(swap=''):
    
    file_type = 'source (SRC)' if not swap else 'swap (SWP)'
    print(f'\033[91m>>><<< Err Specified {file_type} \
file does not exist\033[00m')
    exit()


def src_copy_add_message(directories, src_name):

    if args.verbose and directories:
            print(f'Folders added "{src_name}" successfuly ')   
            for num, item in enumerate(directories, 1):
                print(f'{num}) - {os.path.normpath(item)}')
    elif args.quiet: 
        return None
    else: 
        if directories: 
            print(f'File "{src_name}" copied successfuly to added folders')


def src_copy_message(directories, src_name):
    
    if args.verbose:
            print(f'Copying "{src_name}" in ')
            
            for num, item in enumerate(directories, 1):
                print(f'{num}) - {os.path.normpath(item)}')
    elif args.quiet: 
        return None
    else: 
        print(f'File "{src_name}" copied successfuly to cached folders')

def src_swap_success_message(success, swapfile):

    if not success: 
        print('Failed to swap')
        return None

    if args.verbose: 
        print(f'Swap successful\n"{swapfile}" - is the new source file')
    elif args.quiet: 
        return None
    else:
        print('Swap successful')

def src_delete_message(src):
    if args.verbose:
        print(f'{src} have been removed from the cache file. \
You can no longer update {src}. Add again with a folder to copy to\
use again')
    elif args.quiet:
        return None
    else: 
        print(f'{src} removed from cache. No longer updatable')

def src_same_file_name_switcher(file_list):

    MAX_SIZE = len(file_list)

    print(f'Please select one of the following source files to use\n\
(1) to ({MAX_SIZE}) or enter any other characters to exit program')
    print('\n'.join([f'{num} - {src}' for num, src in enumerate(file_list, 1)]))

    try:
        user_input = int(input("> "))
        return file_list[user_input - 1] 
    except:
        exit()