#!/usr/bin/env python3
import cache
import directories
import sourcefile
from commandparse import args

if __name__ == "__main__":

    cache_d = cache.src_cache_get()
    SRC = sourcefile.src_get(args.source)[0]
    
    if args.add or args.update:
        if args.add: 
            cache_d = sourcefile.src_add(cache_d, SRC, args.add)
        else:
            cache_d = sourcefile.src_update(cache_d, SRC)
    
    elif args.swap: 
        cache_d = sourcefile.src_swap(cache_d, SRC, args.swap)
    
    elif args.remove_dir: 
        cache_d = directories.dirs_remove(cache_d, SRC, args.remove_dir)
    
    elif args.delete:
        cache_d = sourcefile.src_remove(cache_d, SRC)
    
    if args.status: 
        directories.dirs_status(cache_d, SRC)

    cache.src_cache_update(cache_d)



