import datetime
import os.path

is_same_dirs_as_src = lambda dirs, src: os.path.abspath(dirs) == os.path.dirname(os.path.abspath(src))
is_dir_exist_and_accessible = lambda dirs: os.path.isdir(dirs) and os.access(dirs, os.W_OK)
is_file_exist_and_accessible = lambda file: os.path.isfile(file) and os.access(file, os.R_OK)
list_item_common_remove = lambda list_a, list_b: list(set(list_a).difference(set(list_b)))
file_dir_name = lambda file: os.path.dirname(file)
time_elapsed = lambda t_delta: datetime.timedelta(seconds=t_delta.seconds, days=t_delta.days)
ternary_comparision = lambda message_true, message_false, object_1, object_2: message_true if object_1 == object_2 else message_false

