import sys
import os
if __name__ == '__main__':
    from log import *
else:
    from chuprotest.log import *

def add(name, init_dict, default):
    if name in init_dict:
        globals()[name] = init_dict[name]
    else:
        globals()[name] = default
        os.makedirs(os.path.dirname(globals()[name]), exist_ok=True)
    
def init(init_dict={}):
    global path_to_gens, path_to_lib, path_to_texlib, path_to_pdfdir, path_to_main, path_to_prog, log
    
    add('path_to_gens', init_dict, os.path.join(os.path.expanduser("~"),"test/new/"))
    add('path_to_lib', init_dict, os.path.join(os.path.expanduser("~"),"test/lib/chupro.h"))
    add('path_to_texlib', init_dict, os.path.join(os.path.expanduser("~"),"test/tehno/chupro.tex"))
    add('path_to_pdfdir', init_dict, os.path.join(os.path.expanduser("~"),"test/pdf/"))
    add('logdir', init_dict, os.path.join(os.path.expanduser("~"),"test/log/"))
    add('path_to_main', init_dict, os.path.join(os.path.expanduser("~"),"test/main.cpp"))
    add('path_to_prog', init_dict, os.path.join(os.path.expanduser("~"),"test/a.out"))
    add('path_to_pass', init_dict, os.path.join(os.path.expanduser("~"),"test/pass/pass.txt"))
    
    os.makedirs(os.path.dirname(logdir), exist_ok=True)
    log = Log(sys.stdout, True)
    log.set_file(os.path.join(logdir, "log.txt"))
    log.set_file(os.path.join(logdir, ".log.txt"))

init()