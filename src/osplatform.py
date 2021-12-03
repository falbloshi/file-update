import os
import platform

def cache_dir_a_file():

    if platform.system() != "Windows":
    #stackoverflow.com/a/35249327, if you don't copy from sof, what use of you?
        src_cache_dir = os.path.expanduser("~") + ".config/fipdate" 
        src_cache_file = src_cache_dir + "/cache.json"
    else: 
        src_cache_dir = "C:\\ProgramData\\fipdate"
        src_cache_file = src_cache_dir + "\\cache.json"

    return src_cache_dir, src_cache_file
    