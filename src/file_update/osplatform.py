from . import lambdas
import os
import platform

IS_WINDOWS = True if platform.system() == "Windows" else False


def cache_dir_and_file_get():
    if not IS_WINDOWS:
    #stackoverflow.com/a/35249327, if you don't copy from sof, what use of you?
        src_cache_dir = os.path.expanduser("~") + "/.cache/file-update" 
        src_cache_file = src_cache_dir + "/cache.json"
    else: 
        src_cache_dir = "C:\\ProgramData\\File-Update"
        src_cache_file = src_cache_dir + "\\cache.json"
    return src_cache_dir, src_cache_file


def windows_drive_letter_iterate(drive_letter):  
    a = 67
    while a < 91:
        yield chr(a) + drive_letter[1:]
        a += 1


def windows_drive_letter_resolve(copy, cache_file, src, directory):
    """
    This function will check if there is a directory 
    using another drive letter in windows systems.
    """
    if not IS_WINDOWS: 
        return ''
    for path in windows_drive_letter_iterate(copy):
        if lambdas.is_file_exist_and_accessible(path):
            directory.insert(directory.index(copy), path)             
            cache_file[src].update({path: cache_file[src][copy]})
            return f'For "{copy}" drive letter resolved to "{path[:1]}:\\"'
    return ''   