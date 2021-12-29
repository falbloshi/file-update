from .commandparse import args
from . import lambdas
import os.path

num_filter = 0


def dirs_filter_message(directories, filtered_directories, message):

    global num_filter
    
    removed = lambdas.list_item_common_remove(
        set(directories), set(filtered_directories))
    
    if args.verbose:
        if message and removed: print(f"Verifying {message}:")
        
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
            num_filter = num
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
        print('\n'.join((f'{num + num_filter}) - \'{dirs}\' {ms}'
                        for num, dirs in enumerate(ints, 1))))
    elif args.quiet: 
        return None
    else: 
        if ints:
            ms = f'{"One" if len(ints) == 1 else f"Nos. {len(ints)} of"}'
            print(f'{ms} director{"y" if len(ints) == 1 else "ies"} already \
exists in cache')


def dirs_remove_message(dirs_to_remove):

    if args.quiet or not dirs_to_remove: 
        return None
    elif args.verbose:
        print("\n".join((f"{num}) - '{dirs}' removed from cache file" 
                        for num, dirs in enumerate(dirs_to_remove, 1))))
    else: 
        print(f'Director{"y" if len(dirs_to_remove) == 1 else "ies"} \
removed from future updates')


def src_not_existing_message_and_exit(swap=''):
    
    if args.quiet: exit()
    else: 
        file_type = 'source' if not swap else 'swap'
        print(f'\n---> Specified {file_type} file does not exist\n')
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
            print(f'\nCopying "{src_name}" in ')
            
            for num, item in enumerate(directories, 1):
                print(f'{num}) - {os.path.normpath(item)}')
    elif args.quiet: 
        return None
    else: 
        print(f'File "{src_name}" copied successfuly to cached folders')


def src_swap_success_message(success, swapfile):

    if not success: 
        print("Failed to swap")
        return None

    if args.verbose: 
        print(f'Swap successful\n"{swapfile}" - is the new source file')
    elif args.quiet: 
        return None
    else:
        print('Swap successful')
