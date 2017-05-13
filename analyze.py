import os
import re
import sys

if __name__ != '__main__':
    import chuprotest.settings
    settings = chuprotest.settings

def genpvscfg():
    cfg = open(settings.path_to_pvscfg, "w")
    cfg.write("exclude-path = /usr/include/\n")
    cfg.write("platform = linux64\n")
    cfg.write("preprocessor =gcc\n")
    cfg.write("analysis-mode=0\n")
    cfg.write("language = C++\n")
    cfg.write("output-file = " + settings.path_to_pvslog + "\n")
    cfg.write("cl-params = -c -Wall -fpermissive -std=c++11 " + settings.path_to_main + "\n")
    cfg.write("source-file = " + settings.path_to_main + "\n")
    cfg.write("sourcetree-root = " + settings.path_to_test + "\n")

def pvs():
    genpvscfg()
    errors = list()
    code = os.system("pvs-studio --cfg " + settings.path_to_pvscfg)
    if code:
        settings.log.writeln("PVS-Studio analis fail")
    else:
        os.system(
            "plog-converter -a \"GA;OP;CS\" -d V2008,V525,V807 -t tasklist -o " + 
            settings.path_to_pvstasks + " " + settings.path_to_pvslog + " > /dev/null")
        os.system("rm " + settings.path_to_pvslog)
        pvstasks = open(settings.path_to_pvstasks, "r", encoding="cp1251")
        ignorepvs = (
            "lib/chupro.h",
            "visualcpp, clang, gcc, bcc, bcc_clang64",
            "Incorrect value for 'preprocessor' parameter. Corect values are:",
            "Help: The documentation for all analyzer warnings is available here:",
            "to the left and to the right of the '|' operator"
        )
        for i in pvstasks:
            for ignore in ignorepvs:
                if ignore in i:
                    break
            else:
                errors.append(i.strip())
    return errors


def analyse(gen):
    global index
    fgen = open(gen, "r", encoding="cp1251")
    strgen = str()
    index = list()
    longcomments = False
    success = True
    strnum = 1
    for i in fgen:
        symnum = 1
        for j in i:
            index.append((strnum, symnum))
            if j == '\t':
                symnum += 4
            else:
                symnum += 1
        strgen += i
        istrip = i.strip()
        if len(istrip) > 79 and istrip[:2] == "//" and not longcomments:
            longcomments = True
            settings.log.writeln("Комментарии длинее 79 символов")
        strnum += 1
    success = check_regex(strgen)
    return success


def check_regex(strgen):
    success = True
    for i in list_of_patterns:
        for j in re.finditer(i[0], strgen):
            success = False
            settings.log.writeln(str(index[j.start()][0]) + ':' + str(
                index[j.start()][1]) + ' ' + re.sub(wspace, '', j.group()) + '\t\t' + i[1])
    return success


def test_regex():
    tests = [
        "rusogl | tem12345_|'a'",
        "'a'|  'a'",
        "up_|'2'|_up",
        "Привет.\"|_sf",
        "','|_sf",
        "task|tem12345_|\"s\"|_tem",
        "_vf;\nsol | podrob_",
        "task|bhs_ | \"Какой-то текст условия\"",
        "tem12345_|\" важный квант \" |_tem",
        "spec.tire|\' "
    ]
    for i in tests:
        print(i)
        for j in list_of_patterns:
            for k in re.finditer(j[0], i):
                print('\t' + str(k.start()) + '\t' +
                      re.sub(wspace, '', k.group()) + '\t\t' + j[1])
        print()


wspace = "\s*"
quotes = "(\'|\")"  # ",'
symbolindquote = "\".\""  # "a"
lws = wspace + "\|" + wspace
vidn = "vid" + wspace + "==" + wspace + "\d+"
upr = "(bhs_|_bhs_|_bhs|abzac|podrob_|_podrob)"
tem_ = "(tem([0-9]){5}_)"
_tem = "_tem"
tem = "(" + tem_ + "|" + _tem + ")"
tire = "spec\.tire"

list_of_patterns = [
    (quotes + wspace + "\|" + wspace + quotes, "Объединить в одну строку"),  # "|'
    (lws + symbolindquote + wspace + "(\||;)", "Символ добавлять быстрее"),  # |"a"
    # слишком длинный список видов
    ("(" + vidn + "(\s|\|\|)*){6,}", "vidin+list"),
    ("rusogl" + lws + "tem", "rusogl не работает через tem"),
    ("(\.|,)" + wspace + quotes + lws + "_sf",
     "точка/запятая не должны быть в sf"),  # ."|_sf
    ("up_" + lws + quotes + "*" + "(2|3)" + quotes + "*" + \
     lws + "_up", "для этого есть специальный тег upx"),
    ("down_" + lws + quotes + "*" + "(0|1|2)" + quotes + "*" + \
     lws + "_down", "для этого есть специальный тег downx"),
    ("_frac_" + lws + quotes + "*" + "2" + quotes + "*" + \
     lws + "_frac", "для этого есть специальный тег _frac2"),
    ("_vf" + wspace + ";" + wspace + "sol" + lws + \
     "podrob_", "podrob не может быть сразу после vf"),
    (upr + wspace + "\|", "Нужно вывести отдельным выражением"),
    (tem_ + lws + quotes + " " + "|" + " " + quotes + lws + _tem,
     "tem не должна начинаться или заканчиваться пробелом"),
    (tire + lws + quotes + " " + "|" + " " + quotes + \
     lws + tire, "spec.tire расставляет свои пробелы"),
    # ("'(.){2,}'|''", "В ' должен быть ровно один символ")  not for regex
]

if __name__ == '__main__':
    test_regex()
