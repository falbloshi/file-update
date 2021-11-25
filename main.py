import sys
import shutil
import os
import argparse


parser = argparse.ArgumentParser(
        description = 'Updates multiple copies of a file in different directories')

parser.add_argument("source", type=str, metavar="SRC",
                    help="the original file")

parser.add_argument("-d","--dest", metavar="DEST", type=str, nargs='+', required=True,
                    help="destinations of copies")

parser.add_argument("-p", "--path", action="store_true",
                    help="displays the absolute path of the source file")

args = parser.parse_args()

#Checks if source is a file in current working directory or an absolute path, return fullpath and the file name for either
if os.path.isfile(args.source): 
    fullPathSrc = os.path.realpath(args.source)
    baseNameSrc = os.path.basename(args.source)
else: 
    print(f"{args.source} is not a valid file")
    parser.print_help()

#removing non directory listing
args.dest = [dest for dest in args.dest if os.path.isabs(dest)]
print(args.dest)


if args.path and os.path.isfile(args.source):
    print(f"the fullpath name of {baseNameSrc} is {fullPathSrc}")
