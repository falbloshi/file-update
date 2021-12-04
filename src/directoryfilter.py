from lambdafuncs import *
import messages

def dirs_filter(directory):
    dirs = set([dirs for dirs in directory \
            if is_dir_exist_a_accessible(dirs)
            and not is_same_dirs_as_src(dirs, messages.args.source)])
    
    messages.dirs_filter_message(directory, dirs)

    return list(map(os.path.abspath, dirs))

def dirs_existing_filter(directory, new_directories=[]):
    new_directories = dirs_filter(new_directories)

    filtered_directory = [dirs for dirs in directory \
                            if is_dir_exist_a_accessible(dirs)\
                            and dirs not in new_directories]
    
    messages.dirs_existing_filter_message(directory, filtered_directory, new_directories)
     
    return list(map(os.path.abspath, filtered_directory)) +  list(map(os.path.abspath, new_directories))