import datetime
import os.path
from typing import Generator

#The reason why this module is called lambdas
#is I used lambas instead of def 

def is_same_dirs_as_src(dirs, src):
    return os.path.abspath(dirs) == os.path.dirname(os.path.abspath(src))

def is_dir_exist_and_accessible(dirs):
    return os.path.isdir(dirs) and os.access(dirs, os.W_OK)

def is_file_exist_and_accessible(file):
    return os.path.isfile(file) and os.access(file, os.W_OK)

def list_item_common_remove(list_a, list_b):
    return set(list_a).difference(set(list_b))

def file_dir_name(file):
    return os.path.dirname(file)

def time_elapsed(t_delta):
    return datetime.timedelta(seconds=t_delta.seconds, days=t_delta.days)

def ternary_comparision(message_true, message_false, object_1, object_2):
    return message_true if object_1 == object_2 else message_false


