import sys

from util_function import *


def main(args):
    if len(args) == 0:
        print("Missing parameter")
        return
    start = args[0]
    output, df = get_proposals_approved_from_day(start)
    print(df)
    print('check on {}'.format(output))


if __name__ == '__main__':
    main(sys.argv[1:])