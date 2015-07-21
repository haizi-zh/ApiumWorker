# coding=utf-8

__author__ = 'zephyre'


def worker():
    import imp

    from apiumworker.global_conf import parse_cl_args

    project_conf, cmd_args = parse_cl_args()

    for m in project_conf['modules']:
        result = imp.find_module(m)
        module = imp.load_module(m, *result)
        app = module.app.app
        app.worker_main(argv=cmd_args)


if __name__ == '__main__':
    worker()