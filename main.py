import logging
import getopt
import sys

from App import App

def main(args):
    # Defaults
    LOG_LEVEL = 'INFO'

    # Get logging level argument
    try:
        opts, args = getopt.getopt(args, 'l', ['log='])
    except:
        print('Invalid arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--log'):
            LOG_LEVEL = arg

    logging.basicConfig(level=LOG_LEVEL)
    return App()

if __name__ == '__main__':
    main(sys.argv[1:])
