import argparse
from textwrap import dedent

parser = argparse.ArgumentParser(
            description = 
            'Updates multiple copies of a file(SRC) residing in different directories(DIRS)', 
            prog='file-update/fud',
            formatter_class=argparse.RawDescriptionHelpFormatter, epilog=dedent(
            '''cache.json will be stored in /HOME/USER/.cache/file-update
and for Windows systems in C:\\ProgramData\\file-update

The source file resides in www.github.com/falbloushi/file-update

Author: Faris Al-Bloshi 2021
Version: 1.0b0
License: MIT ''')
            )

parser.add_argument('source', type=str, metavar='SRC',
                    help='SRC, the origin source file to be copied. If not exising in cache.json\
                    will create a new entry')

parser.add_argument('-a', '--add', metavar='DIRS', action='extend', type=str, nargs='+', default=None,
                    help='adds directories to copy a SRC file to')

parser.add_argument('-u', '--update', action='store_true',
                    help='update SRC file in stored directories')

parser.add_argument('-s', '--simulate', action='store_true',
                    help='simulate copy process, don\'t perform real changes')

parser.add_argument('--status', action='store_true',
                    help='prints live status of a SRC file and its related copies; displays regardless of -q flag')

parser.add_argument('--swap', metavar='SWP', type=str, nargs='?', default='',
                    help='swaps current source file with that in swap; -a and -u will override --swap')

parser.add_argument('-q', '--quiet', action='store_true',
                    help='display no output')

parser.add_argument('-r', '--remove-dir', metavar='RMDIR', action='extend', type=str, nargs='+',
                    help='removes a copy\'s directory(DIRS) from cache from the specified SRC,\
                    will not delete the real directory; -a and -u will override -r')

parser.add_argument('-d', '--delete', action='store_true',
                    help='deletes an origin file(SRC) from cache, will not delete the real file\
                    ; --swap, -a, -u and -r will override -d')                   

parser.add_argument('-v', '--verbose', action='store_true',
                    help='display more information in output; overrides -q flag')

parser.add_argument('--version', action='version', version='%(prog)s 1.0b0')


args = parser.parse_args()