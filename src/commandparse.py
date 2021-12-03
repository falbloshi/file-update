import argparse

parser = argparse.ArgumentParser(
            description = 
            'Updates multiple copies of a file(SRC)\
            residing in different directories(DIRS)', 
            prog="fipdate",
            epilog = 
            'Files: cache.json will be stored in /HOME/USER/.config/fipdate\
            and for Windows systems in C:\\ProgramData\\fipdate\
            \nThe source file resides in www.github.com/falbloushi/file-update\
            \nAuthor: Faris 2021')

parser.add_argument("source", type=str, metavar="SRC",
                    help="SRC, the origin source file to be copied. If not exising in cache.json\
                    will create a new one")

parser.add_argument("-a", "--add", metavar="DIRS", type=str, nargs='+',
                    help="adds directories to copy an existing SRC file")

parser.add_argument("-u", "--update", action="store_true",
                    help="update existing SRC file")

parser.add_argument("-s", "--simulate", action="store_true",
                    help="simulate copy process, don't perform real changes")

parser.add_argument("--status", action="store_true",
                    help="prints live status of a SRC file and its related copies; displays regardless of -q flag")

parser.add_argument("--swap", metavar="SWP", action="store_true", type=str, nargs="?",
                    help="swaps current source file with that in swap; -a and -u will override --swap")

parser.add_argument("-q", "--quiet", action="store_true",
                    help="display no output")

parser.add_argument("-d", "--delete", metavar="RMSRC", action="store_true",
                    help="deletes an origin file(SRC) from history, will not delete the real file\
                    ; -a and -u will override -d")

parser.add_argument("-r", "--remove", metavar="RMDIR", action="store_true", type=str, nargs='+',
                    help="removes a copy's directory(DIRS) from history from the specified SRC,\
                    will not delete the real directory; -a and -u will override -r")                   

parser.add_argument("-v", "--verbose", action="store_true",
                    help="display more information in output; overrides -q flag")


args = parser.parse_args()