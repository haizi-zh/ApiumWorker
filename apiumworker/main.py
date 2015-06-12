__author__ = 'zephyre'


def worker():
    import argparse
    import imp
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--module', '-m', nargs='*', choices=['sms'])
    args, left_over = parser.parse_known_args()

    for m in args.module:
        result = imp.find_module('sms')
        app = imp.load_module('sms', *result).app.app

        args = sys.argv[:1]
        args.extend(left_over)

        app.worker_main(argv=args)

        print m

if __name__ == '__main__':
    worker()

