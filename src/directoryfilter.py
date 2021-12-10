from lambdafuncs import *
import messages

def dirs_filter(directories, message="added"):
    filtered_directories = list(set([dirs for dirs in directories 
                                    if is_dir_exist_a_accessible(dirs)
                                    and not is_same_dirs_as_src(dirs, messages.args.source)]))
    
    messages.dirs_filter_message(directories, filtered_directories, message)

    return list(map(os.path.abspath, filtered_directories))

def dirs_existing_filter(existing_directories, new_directories=[]):
    new_directories = dirs_filter(new_directories, None)

    filtered_new_directories = [dirs for dirs in new_directories 
                                if dirs not in existing_directories]
    
    messages.dirs_new_filter_message(existing_directories, filtered_new_directories)
     
    return list(map(os.path.abspath, filtered_new_directories))