import sys
import os
if __name__ == '__main__':
    from log import *
else:
    from chuprotest.log import *

def add(name, init_dict, default, **args):
    if name in init_dict:
        globals()[name] = init_dict[name]
    else:
        globals()[name] = default
        if 'path' in args and args['path'] == True:
            os.makedirs(os.path.dirname(globals()[name]), exist_ok=True)
    
def init(init_dict={}):
    global log
    
    add('path_to_gens', init_dict, os.path.join(os.path.expanduser("~"), "test/new/"), path=True)
    add('path_to_lib', init_dict, os.path.join(os.path.expanduser("~"), "test/lib/chupro.h"), path=True)
    add('path_to_texlib', init_dict, os.path.join(os.path.expanduser("~"), "test/tehno/chupro.tex"), path=True)
    add('path_to_pdfdir', init_dict, os.path.join(os.path.expanduser("~"), "test/pdf/"), path=True)
    add('logdir', init_dict, os.path.join(os.path.expanduser("~"), "test/log/"), path=True)
    add('path_to_main', init_dict, os.path.join(os.path.expanduser("~"), "test/main.cpp"), path=True)
    add('path_to_prog', init_dict, os.path.join(os.path.expanduser("~"), "test/a.out"), path=True)
    add('path_to_pass', init_dict, os.path.join(os.path.expanduser("~"), "test/pass/pass.txt"), path=True)
    add('make_pvs', init_dict, False)
    add('make_compile', init_dict, True)
    add('make_tex', init_dict, True)
    add('make_comments', init_dict, True)
    add('make_analyse', init_dict, True)
    add('make_static', init_dict, False)

    os.makedirs(os.path.dirname(logdir), exist_ok=True)
    log = Log(sys.stdout, True)
    log.set_file(os.path.join(logdir, "log.txt"))
    log.set_file(os.path.join(logdir, ".log.txt"))

init()