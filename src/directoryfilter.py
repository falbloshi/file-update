from lambdafuncs import *
import messages

def dirs_filter(directory):
    dirs = set([dirs for dirs in directory \
            if is_dir_exist_a_accessible(dirs)
            and not is_same_dirs_as_src(dirs, messages.args.source)])
    
    messages.dirs_filter_message(directory, dirs)
    
    return list(dirs)

def dirs_existing_filter(directory, new_directory_list=[]):
    #assuming they are keys in cache file 
    directory = [os.path.dirname(dirs) for dirs in directory]

    filtered_directory = [dirs for dirs in directory \
                            if is_dir_exist_a_accessible(dirs)\
                            and dirs not in new_directory_list]
    
    messages.dirs_existing_filter_message(directory, filtered_directory, new_directory_list)

    return filtered_directory + new_directory_list