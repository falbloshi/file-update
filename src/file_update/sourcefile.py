
from . import directoryfilter
from . import messages
from . import lambdas
from . import hashfile
from concurrent.futures import ThreadPoolExecutor
import os.path
import shutil

SIM = messages.args.simulate


def src_get(src):
    """
    Sanity check for source file
    """
    if os.path.isfile(src): 
        src_full_path = os.path.realpath(src)
        src_base_name = os.path.basename(src)
    else: 
        messages.src_not_existing_message_and_exit()
    
    return src_full_path, src_base_name


def src_copy(directories, src):
    """
    Copies the source in the directories specified in 
    either --add or -a flag or stored in the cache file
    """
    if not SIM and directories:
        ThreadPoolExecutor().map(lambda directory: shutil.copy2(
            src, os.path.normpath(directory)), directories) 


def src_add(cache_file, src, dirs_new=None):
    """
    Adds folders to source path in cache file, 
    copies them if they don't exists
    
    If source doesn't exist in the json, add it 
    and the folders mentioned in --add or -a flag
    """
    try:
        file_hash, file_time = hashfile.file_hash_and_time(src)[:2]
        BASE = os.path.basename(src)
        dirs_existing = list(map(lambdas.file_dir_name, cache_file[src]))
        dirs_new = directoryfilter.dirs_existing_filter(dirs_existing, dirs_new)

        for dir_path in dirs_new:
            added_file_path = os.path.join(dir_path, BASE)
            
            if not SIM: cache_file[src].update({added_file_path: 
                                                [file_hash, file_time]})     
        src_copy(dirs_new, src)
        messages.src_copy_add_message(dirs_new, BASE)
    except KeyError or TypeError:
        file_hash, file_time = hashfile.file_hash_and_time(src)[:2]
        directories = directoryfilter.dirs_filter(dirs_new, None)
        
        if directories:
            if not SIM: cache_file[src] = {}

            for dir_path in directories:
                new_file_path = os.path.join(dir_path, os.path.basename(src))
                
                if not SIM: cache_file[src].update({new_file_path: 
                                                    [file_hash, file_time]})
            src_copy(directories, src)
            messages.src_copy_message(directories, os.path.basename(src))
    return cache_file


def src_update(cache_file, src):
    """
    Checks the cache file for folders and update them with 
    the newest iteration of the source file

    Heavy process if files are big 
    """
    file_hash, file_time = hashfile.file_hash_and_time(src)[:2]
    BASE = os.path.basename(src)
    
    try:
        dirs_existing = directoryfilter.dirs_filter(list(map(
            lambdas.file_dir_name, cache_file[src])), "existing")

        for dir_path in dirs_existing:
            updated_file_path = os.path.join(dir_path, BASE)
            
            if not SIM: cache_file[src].update(
                {updated_file_path: [file_hash, file_time]})     
        src_copy(dirs_existing, src)
        messages.src_copy_message(dirs_existing, BASE)
    except KeyError:
        messages.src_not_existing_message_and_exit(src)
    return cache_file


def src_swap(cache_file, src, swap_file):
    """
    Swaps the source file to whatever is in --swap flag, 
    it must have the same file name as source
    """
    
    if not lambdas.is_file_exist_and_accessible(swap_file): 
        messages.src_not_existing_message_and_exit("s")
    
    if os.path.basename(src) == os.path.basename(swap_file):
        try: 
            file_hash, file_time = hashfile.file_hash_and_time(src)[:2]
            swap_path = os.path.abspath(swap_file)
            success = None

            if not SIM:
                if lambdas.is_file_exist_and_accessible(swap_path):
                    cache_file.update({swap_path:cache_file[src]})
                    cache_file[swap_path].update({src: [file_hash, file_time]})
                    
                    if cache_file[swap_path][swap_path]: 
                        del cache_file[swap_path][swap_path]
                    
                    del cache_file[src]
                    success = True
            else: success = True
            
            messages.src_swap_success_message(success, swap_path)
            return cache_file
        except KeyError:
            messages.src_not_existing_message_and_exit()

def src_delete(cache_file, src):
    """
    Removes the source file and its related copies 
    destination from cache, does not deletes 
    the actual file or its copies
    """

    
    if SIM:
        messages.src_delete_message(os.path.basename(src))
        return cache_file
    try:
        del cache_file[src]
        messages.src_delete_message(os.path.basename(src))
        return cache_file
    except KeyError:
        messages.src_not_existing_message_and_exit()
