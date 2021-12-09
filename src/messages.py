from commandparse import args, parser
from lambdafuncs import *


def dirs_filter_message(directories, filtered_directories):
    if not directories: return
    if args.verbose:
        num = 1
        print("\nChecking added:")
        for dirs in list_item_common_remove(set(directories), set(filtered_directories)):
            if is_same_dirs_as_src(dirs, args.source): 
                print(f'{num} - \'{dirs}\' removed - no action to the same directory as the source file')
            elif os.path.isdir(dirs): 
                print(f'{num} - \'{dirs}\' removed - could be missing file mount or user access')
            elif os.path.isabs(dirs): 
                print(f'{num} - \'{dirs}\' removed - could be missing file mount or invalid directory')
            else: 
                print(f'{num} - \'{dirs}\' removed - not a directory')
            num += 1
    elif args.quiet: return
    else: 
        if set(directories) != set(filtered_directories): print('Invalid directories removed')

def dirs_existing_filter_message(existing_directories, filtered_existing_directories, new_directories):
    if args.verbose:
        num = 1    
        if filtered_existing_directories + new_directories: print("\nChecking existing:")
        for dirs in existing_directories:
            if dirs in new_directories: 
                print(f'{num} - \'{dirs}\' removed - already exists')
                num += 1
            elif dirs not in filtered_existing_directories: 
                print(f'{num} - \'{dirs}\' removed - folder does not exist or inaccessible')
                num += 1
    elif args.quiet: return
    else: 
        if set(existing_directories) != set(filtered_existing_directories): print('Invalid directories removed')

def dirs_remove_message(dirs_to_remove):
    if args.verbose:
        num = 1
        for each in list(dirs_to_remove):
            print(f'{num} - \'{each}\' removed from from source')
    elif args.quiet: return
    else: 
        print(f'Directories removed from future updates')

def source_not_existing_message_a_exit(swap=''):
    if args.quiet: exit()
    else: 
        file_type = 'source' if not swap else 'swap'
        print(f'\n---> Specified {file_type} file does not exist\n')
        parser.print_help()
        exit()

def src_copy_add_message(directories, src_name):
    if not directories: return
    if args.verbose:
            print(f'\nFolders added "{src_name}" successfuly ')
            num = 1
            for item in directories:
                print(f'{num} - {os.path.normpath(item)}')
                num += 1
    elif args.quiet: return
    else: print(f'File "{src_name}" copied successfuly to new folders')


def src_copy_message(directories, src_name):
    if args.verbose:
            print(f'\nCopying "{src_name}" in ')
            num = 1
            for item in directories:
                print(f'{num} - {os.path.normpath(item)}')
                num += 1
    elif args.quiet: return
    else: print(f'File "{src_name}" copied successfuly to cached folders')
    
def  src_cache_get_message(src_cache_dir):
    if not args.quiet:
        print(f'Cache file did not exist. Creating cache.json in {src_cache_dir}')