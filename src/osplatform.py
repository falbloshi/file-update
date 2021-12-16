import os
import platform

IS_WINDOWS = True if platform.system() == "Windows" else False

def cache_dir_and_file_get():

    if not IS_WINDOWS:
    #stackoverflow.com/a/35249327, if you don't copy from sof, what use of you?
        src_cache_dir = os.path.expanduser("~") + "/.config/fipdate" 
        src_cache_file = src_cache_dir + "/cache.json"
    else: 
        src_cache_dir = "C:\\ProgramData\\fipdate"
        src_cache_file = src_cache_dir + "\\cache.json"
    
    return src_cache_dir, src_cache_file


def windows_drive_letter_resolve(path):
    if not IS_WINDOWS: return
    a = 66
    while a < 91:
        yield chr(a) + path[1:]
        a += 1
