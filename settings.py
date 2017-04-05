import sys
import os
if __name__ == '__main__':
    from log import *
else:
    from chuprotest.log import *
    
def init(init_dict={}):
    global path_to_gens, path_to_lib, path_to_texlib, path_to_pdfdir, path_to_main, path_to_prog, log
    
    if 'path_to_gens' in init_dict:
        path_to_gens = init_dict['path_to_gens']
    else:
        path_to_gens = os.path.join(os.path.expanduser("~"),"test/new/")
        os.makedirs(os.path.dirname(path_to_gens), exist_ok=True)
    
    if 'path_to_lib' in init_dict:
        path_to_lib = init_dict['path_to_lib']
    else:
        path_to_lib = os.path.join(os.path.expanduser("~"),"test/lib/chupro.h")
        os.makedirs(os.path.dirname(path_to_lib), exist_ok=True)
    
    if 'path_to_texlib' in init_dict:
        path_to_texlib = init_dict['path_to_texlib']
    else:
        path_to_texlib = os.path.join(os.path.expanduser("~"),"test/tehno/chupro.tex")
        os.makedirs(os.path.dirname(path_to_texlib), exist_ok=True)
    
    if 'path_to_pdfdir' in init_dict:
        path_to_pdfdir = init_dict['path_to_pdfdir']
    else:
        path_to_pdfdir = os.path.join(os.path.expanduser("~"),"test/pdf/")
        os.makedirs(os.path.dirname(path_to_pdfdir), exist_ok=True)
    
    if 'logdir' in init_dict:
        logdir = init_dict['logdir']
    else:
        logdir = os.path.join(os.path.expanduser("~"),"test/log/")
    
    if 'path_to_main' in init_dict:
        path_to_main = init_dict['path_to_main']
    else:
        path_to_main = os.path.join(os.path.expanduser("~"),"test/main.cpp")
        os.makedirs(os.path.dirname(path_to_main), exist_ok=True)
    
    if 'path_to_prog' in init_dict:
        path_to_prog = init_dict['path_to_prog']
    else:
        path_to_prog = os.path.join(os.path.expanduser("~"),"test/a.out")
        os.makedirs(os.path.dirname(path_to_prog), exist_ok=True)
        
    os.makedirs(os.path.dirname(logdir), exist_ok=True)
    log = Log(sys.stdout, True)
    log.set_file(os.path.join(logdir, "log.txt"))
    log.set_file(os.path.join(logdir, ".log.txt"))

init()