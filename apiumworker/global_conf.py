# coding=utf-8

__author__ = 'zephyre'


def parse_cl_args():
    """
    解析命令行参数
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--module', '-m', nargs='*', choices=['sms', 'contact', 'message'])
    # parser.add_argument('--runlevel', choices=['production', 'dev', 'test'])
    extracted_args, left_over = parser.parse_known_args()

    args = sys.argv[:1]
    args.extend(left_over)

    return {'modules': extracted_args.module}, args
