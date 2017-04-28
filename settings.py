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
        if 'path' in args and args['path']:
            os.makedirs(os.path.dirname(globals()[name]), exist_ok=True)


def init(init_dict={}):
    global log, already_init
    already_init = True
    home = os.path.expanduser("~")
    add('path_to_home', init_dict, home, path=True)
    add('path_to_test', init_dict, os.path.join(home, 'test/'), path=True)
    
    add('path_to_gens', init_dict, os.path.join(home, 'test/new/'), path=True)
    add('path_to_lib', init_dict, os.path.join(
        home, 'test/lib/chupro.h'), path=True)
    add('path_to_texlib', init_dict, os.path.join(
        home, 'test/tehno/chupro.tex'), path=True)
    add('path_to_pdfdir', init_dict, os.path.join(home, 'test/pdf/'), path=True)
    add('logdir', init_dict, os.path.join(home, 'test/log/'), path=True)
    add('path_to_main', init_dict, os.path.join(
        home, 'test/main.cpp'), path=True)
    add('path_to_prog', init_dict, os.path.join(home, 'test/a.out'), path=True)
    add('path_to_pass', init_dict, os.path.join(
        home, 'test/pass/pass.txt'), path=True)
    add('path_to_gcclog', init_dict, os.path.join(
        home, 'test/gcclog.txt'), path=True)
    add('path_to_cllog', init_dict, os.path.join(
        home, 'test/cllog.txt'), path=True)
    add('path_to_gztex', init_dict, os.path.join(home, 'test/gz.tex'), path=True)
    add('path_to_cl', init_dict, os.path.join(
        home, 'test/testwin/VC/bin/cl.exe'), path=True)
    add('path_to_testwin', init_dict, os.path.join(
        home, 'test/testwin/'), path=True)
    add('path_to_pvscfg', init_dict, os.path.join(home, 'test/PVS-Studio.cfg'), path=True)
    add('path_to_pvstasks', init_dict, os.path.join(home, 'test/pvs.tasks'), path=True)
    add('path_to_pvslog', init_dict, os.path.join(home, 'test/pvs.log'), path=True)
    add('path_to_tmpprep', init_dict, os.path.join(home, 'test/tmpanalis.cpp'), path=True)
    add('make_pvs', init_dict, True)
    add('make_compilegcc', init_dict, True)
    add('make_compilecl', init_dict, True)
    add('make_tex', init_dict, True)
    add('make_comments', init_dict, True)
    add('make_analyse', init_dict, True)
    add('make_static', init_dict, True)

    os.makedirs(os.path.dirname(logdir), exist_ok=True)
    log = Log(os.path.join(logdir, 'log.txt'))
    log.set_file(os.path.join(logdir, '.log.txt'))


def default_init():
    if not already_init:
        init()


already_init = False
