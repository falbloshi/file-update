from . import messages
from . import lambdas
from . import hashfile
from .directoryfilter import dirs_filter
from .osplatform import windows_drive_letter_resolve
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor
import os.path


def dirs_remove(cache_file, src, directories):
    """
    Removes directories in the cache file, 
    does not remove actual copies
    """
    try:
        directories = dirs_filter(directories, None)
        dirs_existing = list(map(lambdas.file_dir_name, cache_file[src]))
        dirs_to_remove = list(
            set(directories).intersection(set(dirs_existing)))
        dirs_to_remove = [os.path.join(file_path, os.path.basename(src)) for
                          file_path in dirs_to_remove]

        for dirs in dirs_to_remove:
            del cache_file[src][dirs]
        messages.dirs_remove_message(dirs_to_remove)
        return cache_file
    except KeyError:
        messages.src_not_existing_message_and_exit()


def dirs_status(cache_file, src):
    """
    Prints actual live status of copies, 
    perform no changes, overrides quiet
    """
    try:
        dirs_copies = list(cache_file[src])
        src_hash, src_build_time, path = hashfile.file_hash_and_time(src)
        print(f'\nOriginal\'s build time: \
{dt.ctime(dt.fromtimestamp(src_build_time))}\nOriginal\'s hash \
value: {src_hash}', end='\n')

        for count, copy in enumerate(dirs_copies.copy(), 1):
            if lambdas.is_file_exist_and_accessible(copy):
                continue
            else:
                count -= 1
                resolve = windows_drive_letter_resolve(
                    copy, cache_file,
                    src, dirs_copies)
                dirs_copies = dirs_delete_missing_prompt(src, count, 
                                dirs_copies, copy, resolve, cache_file)

        results = ThreadPoolExecutor().map(hashfile.file_hash_and_time,
                                           dirs_copies)

        for count, hash_and_build in enumerate(results, 1):
            copy_hash, copy_build_time, path = hash_and_build
            diff_hash = lambdas.ternary_comparision(
                'Equal hash value', 'Unequal hash value', copy_hash, src_hash)
            t_delta = lambdas.time_elapsed(dt.today()
                                           - dt.fromtimestamp(copy_build_time))
            verdict = lambdas.ternary_comparision(
                'Update not needed', 'Update recommended',
                'Equal hash value', diff_hash)

            if not messages.args.verbose:
                copy_hash = f'{copy_hash[:5]}..{copy_hash[-5:]}'

            print(f'\n{count}) {copy_hash} {diff_hash}\
\n{dt.ctime(dt.fromtimestamp(copy_build_time))} \
:: {str(t_delta)} time elapsed from last update\
\n{verdict} for the copy in {lambdas.file_dir_name(path)}', end='\n')
    except KeyError:
        messages.src_not_existing_message_and_exit()
    return cache_file


def dirs_delete_missing_prompt(src, count, dirs_copies, copy, 
                                resolve, cache_file):
    """
    Deletes missing file paths from cache
    if user accepts to remove
    otherwise they stay in cache
    """
    print(f'\n{count}) "{copy}" folder does not exists or \
            inaccessible. {resolve}')

    if not resolve:
        print(f'\nNote, if you don\'t remove the file path now, \
                other operations will still consider this path an existing path\
                in cache. Would you like to remove the path \
                from future updates? [y/n (default)]:')

        if str.lower(input("> ")) == 'y':
            del cache_file[src][copy]
    else: 
        del cache_file[src][copy]
    
    dirs_copies.remove(copy)
    return dirs_copies
    

