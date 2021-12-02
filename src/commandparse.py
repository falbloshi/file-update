import argparse

def command_parser():
    parser = argparse.ArgumentParser(
            description = 'Updates multiple copies of a file(SRC) residing in different directories(DIRS)')

    parser.add_argument("source", type=str, metavar="SRC",
                        help="SRC, the origin source file to be copied")

    parser.add_argument("-a", "--add", metavar="DIRS", type=str, nargs='+',
                        help="adds directories to copy an existing SRC file")

    parser.add_argument("-u", "--update", action="store_true",
                        help="update existing SRC file")

    parser.add_argument("-s", "--simulate", action="store_true",
                        help="simulate copy process, don't perform real changes")

    parser.add_argument("--status", action="store_true",
                        help="prints live status of a SRC file and its related copies; overrides -q flag")
    
    parser.add_argument("--swap", metavar="SWP", action="store_true", type=str, nargs="?",
                        help="prints live status of a SRC file and its related copies; overrides -q flag")

    parser.add_argument("-q", "--quiet", action="store_true",
                        help="display no output")

    parser.add_argument("-d", "--delete", metavar="SRC", action="store_true",
                        help="deletes an origin file(SRC) from history, will not delete the real file")
    
    parser.add_argument("-r", "--remove", metavar="DIRS", action="store_true", type=str, nargs='+',
                        help="removes a copy's directory(DIRS) from history from the specified SRC, will not delete the real directory")                   

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="display more information in output")


    return parser.parse_args()