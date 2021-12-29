from . import lambdas
from . import messages
import os.path

def dirs_filter(directories, message="added"):
    """
    Filters cli argument entries or cache file entries, 
    checks if they exist and accessible and if they are not 
    the same directory as the source
    """
    filtered_directories = list(set([dirs for dirs in directories 
                                    if lambdas.is_dir_exist_and_accessible(dirs)
                                    and not lambdas.is_same_dirs_as_src(
                                        dirs, messages.args.source)]))   
    messages.dirs_filter_message(directories, filtered_directories, message)
    return list(map(os.path.abspath, filtered_directories))


def dirs_existing_filter(existing_directories, new_directories):
    """
    Filters cli argument entries, 
    extracts newly added folders exclusively
    """
    new_directories = dirs_filter(new_directories)
    messages.dirs_new_filter_message(existing_directories, new_directories)
    filtered_new_directories = [dirs for dirs in new_directories 
                                if dirs not in existing_directories]
    return list(map(os.path.abspath, filtered_new_directories))