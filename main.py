from posixpath import BASEname
import shutil
import os
import argparse


def command_parser():
    parser = argparse.ArgumentParser(
            description = 'Updates multiple copies of a file(SRC) residing in different directories(DIRS)')

    parser.add_argument("source", type=str, metavar="SRC",
                        help="the original file")

    parser.add_argument("-d","--dirs", metavar="DIRS", type=str, nargs='+', required=True,
                        help="directory of the copies")

    parser.add_argument("-p", "--path", action="store_true",
                        help="displays the absolute path of the source file")

    parser.add_argument("-s", "--simulate", action="store_true",
                        help="simulate copy process, don't perform real changes")

    parser.add_argument("-q", "--quiet", action="store_true",
                        help="display no output")

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="display more information in output")

    args = parser.parse_args()
    return args
args = command_parser()

#checks if source is a file in current working directory or an absolute path
def get_source():
    if os.path.isfile(args.source): 
        fullPathSrc = os.path.realpath(args.source)
        baseNameSrc = os.path.basename(args.source)
    else: 
        print(f"{args.source} is not a valid file")
        args.print_help()
        exit()
    return fullPathSrc, baseNameSrc

SRC, BASE = get_source()
is_same_dirs_as_src = lambda dirs: os.path.normpath(dirs) == os.path.dirname(SRC)


#removing non directory listing to process reachable and unreachable paths
def dirs_remove_unwanted():
    dirs = [dirs for dirs in args.dirs if os.path.isdir(dirs) and os.access(dirs, os.R_OK) and not is_same_dirs_as_src(dirs)]

    if args.path and os.path.isfile(args.source):
        print(f"the fullpath name of {BASE} is {SRC}")

    if args.verbose:
        num = 1
        for item in list(set(args.dirs)-set(dirs)):
            if is_same_dirs_as_src(item): 
                print(f"{num} - \"{item}\" removed - cannot copy to the same directory as the source file")
            elif os.path.isdir(item): 
                print(f"{num} - \"{item}\" removed - could be missing file mount or file access")
            elif os.path.isabs(item): 
                print(f"{num} - \"{item}\" removed - could be missing file mount or invalid directory")
            else: 
                print(f"{num} - \"{item}\" removed - not a directory")
            num += 1
    elif args.quiet: pass
    else: print("Invalid dirs removed")

    return dirs


def src_copy_to_dirs():
    directories = dirs_remove_unwanted()
    if not args.simulate:
        for directory in directories:
            shutil.copy2(SRC, os.path.normpath(directory))

    if args.verbose:
        print(f"\nCopying {BASE} in ")
        num = 1
        for item in directories:
            print(f"{num} - {os.path.normpath(item)}")
            num += 1
    elif args.quiet: pass
    else: print(f"File {BASE}, Copied Sucessfuly")
    return directories


src_copy_to_dirs()

