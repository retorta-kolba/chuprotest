import subprocess
import time
import os

if __name__ == '__main__':
    from log import *
    import settings
else:
    import chuprotest.settings
    settings = chuprotest.settings


def compilegcc(gen):
    # main generation
    gen_main(gen, 100)
    # compile
    code = os.system("g++-4.9 -std=c++11 -Wextra -Wpedantic -Wall"
                     "  -fpermissive " + settings.path_to_main +
                     " -o " + settings.path_to_prog + " 2> " +
                     settings.path_to_gcclog)
    if code:
        settings.log.writeln("ОШИБКА компиляции gcc")
        # ошибки компилятора
        gccinf = gcclog(gen)
        for i in gccinf:
            settings.log.writeln(i)
    else:
        # предупреждения компилятора
        gccinf = gcclog(gen)
        if len(gccinf) > 0:
            settings.log.writeln("ПРЕДУПРЕЖДЕНИЯ gcc:")
        for i in gccinf:
            settings.log.writeln(i)
        prog_code = os.system("cd " + os.path.dirname(settings.path_to_prog) + " && " +
                  "timeout 10 ./" + os.path.basename(settings.path_to_prog) + " > " +
                  settings.path_to_gztex)
        if prog_code:
            settings.log.writeln("Выполнение программы происходит слишком долго")
    return code


def compilecl(gen):
    gen_main(gen, 100, False, False)  # mvcc + win
    code = os.system("export TESTWIN=\"" + settings.path_to_testwin + "\" && "
                     "export INCLUDE=\"$TESTWIN/VC/include;$TESTWIN/win8sdk/Include/shared/;$TESTWIN/win8sdk/Include/um/;$TESTWIN/win8sdk/Include/winrt/;$TESTWIN/10/Include/10.0.10150.0/ucrt/\" && "
                     "export LIB=\"$TESTWIN/VC/lib;$TESTWIN/win8sdk/Lib/winv6.3/um/x86;$TESTWIN/10/Lib/ucrt/x86\" && "
                     "wine " + settings.path_to_cl + " /EHsc /Wall /W4 z:" +
                     settings.path_to_main + " 2> /dev/null "
                     " | enconv > " + settings.path_to_cllog)
    return code


def compile_tex(gen):
    os.system("enconv -x CP1251 -L ru " + settings.path_to_gztex)
    tex_success = os.system("export HOME=" + os.path.expanduser("~") + " && "
                            "cd " + os.path.dirname(settings.path_to_prog) + " && " +
                            "timeout 10 pdflatex -output-directory=" + settings.path_to_pdfdir +
                            " --jobname=" + os.path.basename(gen)[:-2] + " " + settings.path_to_texlib +
                            " > /dev/null")
    if tex_success == 0:
        settings.log.writeln("Сборка tex прошла успешно")
    else:
        settings.log.writeln("Ошибки в сборке тех")
    os.system("find " + settings.path_to_pdfdir + " \! -name \"*.pdf\""
              " -type f -delete")
    return 1


def check_comments(gen):
    patterns = ["//z:", "//s:", "//re:", "TODO", "todo"]
    findcomment = False
    info = str()
    for i in patterns:
        if(find(gen, i)):
            if not findcomment:
                findcomment = True
                info += "найдено "
            info += i + " "
    return findcomment, info


def gen_main(matfiz, problems, gcc=True, lnx=True):
    f = open(settings.path_to_main, 'w', encoding='utf-8')
    f.write(
        "// This is a personal academic project. Dear PVS-Studio, please check it.\n")
    f.write(
        "// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com\n\n")
    f.write("// сгенерировано автоматически с помощью compilelib.py\n\n")
    f.write("#define _PRINT_STDOUT_CODE_WIN_\n")
    if lnx:
        f.write("#define _LIB_LNXRTL_\n")
    else:
        f.write("#define _LIB_WINRTL_\n")
    if gcc:
        f.write("#define __COMPIL_GCC__\n")
    else:
        f.write("#define __COMPIL_MSVS__\n")
    f.write("#include \"" + settings.path_to_lib + "\"\n")
    f.write("#include \"" + matfiz + "\"\n\n")
    f.write("__GZ_MAIN__(psa)\n{\n")
    f.write("\tGZ_UTIL_DRAFTEST lim;\n")
    f.write("\tlim.test = 1000;\n")
    f.write("\tlim.all_min = " + str(problems) + ";\n")
    f.write("\tlim.vid_min = 10;\n")
    f.write("\tlim.vidopans_min=10;\n")
    f.write("\tlim.vidopans_max=10;\n")
    f.write("\tlim.vid_max = 10;\n")
    f.write("\tgz_util_draftest(lim);\n}\n")


def check_tex():
    errors = set()
    error = False
    tex = open(settings.path_to_gztex, "r", encoding='cp1251')
    for i in tex:
        if "ERRORS" in i:
            error = True
            er = i.split('{')[1].split('}')[0]
            for j in er.split('.'):
                if j.strip() not in errors:
                    errors.add(j)
    return error, errors


def find(mat, pattern):
    f = open(mat, 'r', encoding='cp1251')
    for i in f:
        if pattern in i:
            return True
    return False


def cllog(task):
    clog = open(settings.path_to_cllog, 'r', encoding='utf-8')
    clinf = list()
    for i in clog:
        if task in i:
            clinf.append(i.replace('\n', ''))
    return clinf


def gcclog(task):
    glog = open(settings.path_to_gcclog, "rb")
    good = (task, "error")
    ignore = ("note: in expansion of macro __GZ3__",
              " In static member function static void _GZ_",
              "warning: suggest parentheses around arithmetic in operand of |",
              "required from here"
              )
    gccinf = list()
    for i in glog:
        i = str(i).replace("\\xe2", "").replace("\\x80", "").replace(
            "\\x98", "").replace("\\x99", "")[2:-3]
        for kw in good:
            if kw in i:

                for bw in ignore:
                    if bw in i.replace('\'', ''):
                        break
                else:
                    gccinf.append(i)
                break
    return gccinf
