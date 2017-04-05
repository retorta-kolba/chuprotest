# -*- coding: cp1251 -*-
import subprocess
import time
import os

if __name__ == '__main__':
    from log import *
    import settings
else:
    import chuprotest.settings
    settings = chuprotest.settings


def compile(gen):
    # print(gen)
    # main generation
    gen_main(gen, 100)
    # compile
    if os.system("g++-4.9 -std=c++11 -Wextra -Wpedantic -Wall"
                 "  -fpermissive " + settings.path_to_main + 
                 " -o " + settings.path_to_prog + " 2> gcclog.txt "):
        settings.log.writeln("������ ����������")
        # ������ �����������
        gccinf = gcclog(gen)
        for i in gccinf:
            settings.log.writeln(i)
        return 0
    else:
        settings.log.writeln("���������� ������ �������")
        # �������������� �����������
        gccinf = gcclog(gen)
        if len(gccinf) > 0:
            settings.log.writeln("�������������� �����������:")
        for i in gccinf:
            settings.log.writeln(i)
        os.system("cd " + os.path.dirname(settings.path_to_prog) + " && " +
                  "./" + os.path.basename(settings.path_to_prog) + " > gz.tex")
        os.system("enconv -x CP1251 -L ru gz.tex")
        # TODO: timeout!!
        tex_success = os.system("cd " + os.path.dirname(settings.path_to_prog) + " && " +
                                "pdflatex -output-directory=" + settings.path_to_pdfdir +
                                " --jobname=" + gen[:-2] + " " + settings.path_to_texlib + " ")
        if tex_success == 0:
            settings.log.writeln("������ tex ������ �������")
        else:
            settings.log.writeln("������ � ������ ���")
        os.system("find " + settings.path_to_pdfdir + " \! -name \"*.pdf\""
                         " -type f -delete")
        return 1


def check_comments(gen):
    patterns = ["//z:", "//s:", "//re:"]
    findcomment = False
    info = str()
    for i in patterns:
        if(find(gen, i)):
            if not findcomment:
                findcomment = True
                info += "������� "
            info += i + " "
    return findcomment, info


def gen_main(matfiz, problems):
    f = open(settings.path_to_main, 'w')
    f.write("// This is a personal academic project. Dear PVS-Studio, please check it.\n")
    f.write("// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com\n\n")
    f.write("//������������� ������������� � ������� compilelib.py\n\n")
    f.write("#define _LIB_LNXRTL_\n")
    f.write("#define __COMPIL_GCC__\n")
    f.write("#include \"" + settings.path_to_lib + "\"\n")
    f.write("#include \"" + os.path.join(settings.path_to_gens, matfiz) + "\"\n\n")
    f.write("__GZ_MAIN__(psa)\n{\n")
    f.write("\tGZ_UTIL_DRAFTEST lim;\n")
    f.write("\tlim.test = 1000;\n")
    f.write("\tlim.all_min = "+str(problems)+";\n")
    f.write("\tlim.vid_min = 10;\n")
    f.write("\tlim.vidopans_min=10;\n")
    f.write("\tlim.vidopans_max=10;\n")
    f.write("\tlim.vid_max = 10;\n")
    f.write("\tgz_util_draftest(lim);\n}\n")


def check_tex(mat):
    errors = set()
    error = False
    tex = open("gz.tex", "r", encoding='cp1251')
    for i in tex:
        if "ERRORS" in i:
            error = True
            er = i.split('{')[1].split('}')[0]
            for j in er.split('.'):
                if j.strip() not in errors:
                    errors.add(j)
    return error, errors


def find(mat, pattern):
    f = open(settings.path_to_gens+mat, 'r', encoding='cp1251')
    for i in f:
        if pattern in i:
            return True
    return False


def gcclog(task):
    glog = open("gcclog.txt", "rb")
    good = (task, "error")
    ignore = ("note: in expansion of macro \\xe2\\x80\\x98__GZ3__",
              " In static member function \\xe2\\x80\\x98static void _GZ_",
              "warning: suggest parentheses around arithmetic in operand of \\xe2\\x80\\x98|\\xe2\\x80\\x99",
              "required from here\\n"
              )
    gccinf = list()
    for i in glog:
        i = str(i)
        for kw in good:
            if kw in i:

                for bw in ignore:
                    # print(bw, i, bw in i) 
                    if bw in i:
                        break
                else:
                    gccinf.append(i)
                break
    return gccinf
    