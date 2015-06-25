from apiumworker.etcd_conf import project_conf, cmd_args

__author__ = 'zephyre'


def worker():
    import imp

    for m in project_conf['modules']:
        result = imp.find_module(m)
        app = imp.load_module(m, *result).app.app
        app.worker_main(argv=cmd_args)

if __name__ == '__main__':
    worker()