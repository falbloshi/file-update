from .commandparse import args, parser
from . import lambdas
import os.path

def dirs_filter_message(directories, filtered_directories, message):
    if not filtered_directories: return
    
    if args.verbose:
        num = 1
        
        if message: print(f"\nChecking {message}:")
        
        for dirs in lambdas.list_item_common_remove(set(directories), set(filtered_directories)):
            if lambdas.is_same_dirs_as_src(dirs, args.source): 
                print(f'{num}) - \'{dirs}\' removed - no action to the same directory as the source file')
            
            elif os.path.isdir(dirs): 
                print(f'{num}) - \'{dirs}\' removed - could be missing file mount or user access')
            
            elif os.path.isabs(dirs): 
                print(f'{num}) - \'{dirs}\' removed - could be missing file mount or invalid directory')
            
            else: 
                print(f'{num}) - \'{dirs}\' removed - not a directory')
            
            num += 1
    
    elif args.quiet: return
    
    else:  
        if set(directories) != set(filtered_directories): print('Invalid directories removed')

def dirs_new_filter_message(existing_directories, filtered_new_directories):
    intersect = (set(existing_directories).intersection(set(filtered_new_directories)))
    
    if args.verbose:
        print("\n".join((f"{num}) - '{dirs}' removed - already exists in cache" for num, dirs \
            in enumerate(intersect, 1))))
    
    elif args.quiet: return
    
    else: 
        if intersect: 
            print(f'{len(intersect)} director{"y" if len(intersect) == 1 else "ies"} already exists in cache')

def dirs_remove_message(dirs_to_remove):
    if args.verbose:
        print("\n".join((f"{num}) - '{dirs}' removed from cache" for num, dirs in enumerate(dirs_to_remove, 1))))
    
    elif args.quiet: return
    
    else: 
        print(f'Director{"y" if len(dirs_to_remove) == 1 else "ies"} removed from future updates')

def src_not_existing_message_and_exit(swap=''):
    if args.quiet: exit()
    
    else: 
        file_type = 'source' if not swap else 'swap'
        
        print(f'\n---> Specified {file_type} file does not exist\n')
        
        parser.print_help()
        
        exit()

def src_copy_add_message(directories, src_name):
    if args.verbose and directories:
            print(f'\nFolders added "{src_name}" successfuly ')
            
            num = 1
            
            for item in directories:
                print(f'{num}) - {os.path.normpath(item)}')
                
                num += 1

    elif args.quiet: return
    
    else: 
        if directories: 
            print(f'File "{src_name}" copied successfuly to new folders')
        
        else: 
            print(f"Selected folders cannot be added")


def src_copy_message(directories, src_name):
    if args.verbose:
            
            print(f'\nCopying "{src_name}" in ')
            
            num = 1
            
            for item in directories:
            
                print(f'{num}) - {os.path.normpath(item)}')
            
                num += 1
    
    elif args.quiet: return
    
    else: 
        print(f'File "{src_name}" copied successfuly to cached folders')
    
def src_swap_success_message(success, swapfile):
    if not success: 
        print("Failed to swap")
    
    if args.verbose: 
        print(f'Swap successful\n"{swapfile}" - is the new source file')
    
    elif args.quiet: return 
    
    else: print('Swap successful')
