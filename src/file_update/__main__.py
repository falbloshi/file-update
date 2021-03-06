from . import cache
from . import directories
from . import sourcefile
from .commandparse import args

def start():
    cache_d = cache.src_cache_get()
    
    SRC = sourcefile.src_get(cache_d, args.source)[0]

    if args.add or args.update:
        cache_d = sourcefile.src_add(cache_d, SRC, args.add) if \
                  args.add else sourcefile.src_update(cache_d, SRC)
    elif args.swap: 
        cache_d = sourcefile.src_swap(cache_d, SRC, args.swap)
    elif args.remove_dir: 
        cache_d = directories.dirs_remove(cache_d, SRC, args.remove_dir)
    elif args.delete:
        cache_d = sourcefile.src_delete(cache_d, SRC)
    
    if args.status: 
        cache_d = directories.dirs_status(cache_d, SRC)
    elif args.list:
        directories.dirs_list(cache_d)

    cache.src_cache_update(cache_d)


