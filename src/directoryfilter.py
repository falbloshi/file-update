from lambdafuncs import *
import messages

def dirs_filter(directories):
    filtered_directories = list(set([dirs for dirs in directories \
            if is_dir_exist_a_accessible(dirs)
            and not is_same_dirs_as_src(dirs, messages.args.source)]))
    
    messages.dirs_filter_message(directories, filtered_directories)

    return list(map(os.path.abspath, filtered_directories))

def dirs_existing_filter(directories, new_directories=[]):
    new_directories = dirs_filter(new_directories)

    filtered_directories = [dirs for dirs in directories \
                            if is_dir_exist_a_accessible(dirs)\
                            and dirs not in new_directories]
    
    messages.dirs_existing_filter_message(directories, filtered_directories, new_directories)
     
    return list(map(os.path.abspath, filtered_directories)),  list(map(os.path.abspath, new_directories))