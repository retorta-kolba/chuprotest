import rarfile
import os
import re

if __name__ != '__main__':
    import chuprotest.settings as settings
    import chuprotest.compilelib as compilelib
    import chuprotest.analyze as analyse
    import chuprotest.helper as helper

# TODO: my_error
def password(prog):
    try:
        passfile = open(settings.path_to_pass,'r',encoding='cp1251')  # cp-1251?
    except FileNotFoundError:
        raise RuntimeError("Файл с паролем не найден")
    for i in passfile:
        if i.split('=')[0].strip() == prog:
            passfile.close()
            return i.split('=')[1].strip()
    else: 
        passfile.close()
        raise RuntimeError("Проблеы с паролем: пароль не найден.")

def unrar(path_to_arx, prog):
    try:
        prog_pass = password(prog)
    except RuntimeError:
        raise
    except:
        raise RuntimeError("Ошибка определения пароля для пользователя")
    try:
        rf = rarfile.RarFile(path_to_arx)
    except:
        raise RuntimeError("Проблема с архивом")
    
    if(not rf.needs_password()):
        settings.log.writeln("warning: Программист не зашифровал файл")
    
    try:
        rf.setpassword(prog_pass)
    except rarfile.BadRarFile as err:
        raise RuntimeError('error: rarfile.BadRarFile '+str(err))
        
    try:
        rf.extractall(path=settings.path_to_gens) 
    except:
        raise RuntimeError("Проблема с распаковкой архива")

def cleandir(dirname):
    files = [f for f in os.listdir(path=dirname) if os.path.isfile(os.path.join(dirname, f))]
    for i in files:
        os.remove(os.path.join(dirname, i))

def testgen(gen):
    settings.default_init()
    settings.log.writeln()
    settings.log.writeln(os.path.basename(gen))
    settings.log.write_time()

    if settings.make_compile:
        compile_success = compilelib.compile(gen)
        if compile_success and settings.make_tex:
            tex_success = compilelib.compile_tex(gen)
            if tex_success:
                error_tex, errors_tex_list = compilelib.check_tex()
                if error_tex:
                    settings.log.writeln("Есть ОШИБКИ tex:")
                for i in errors_tex_list:
                    i = i.strip()
                    if len(i)>0:
                        settings.log.writeln(i)
                        

    if settings.make_comments:
        findcomment, info = compilelib.check_comments(gen)
        if findcomment:
            settings.log.writeln(info)
            
    if settings.make_analyse:
        analyse_success = analyse.analyse(gen)

def test():
    settings.default_init()
    gens = [i for i in os.listdir(path=settings.path_to_gens) if os.path.isfile(os.path.join(settings.path_to_gens, i))]
    tasks = list()
    for i in gens:
        path_to_gen = os.path.join(settings.path_to_gens, i)
        if os.path.isfile(path_to_gen) and re.match(r"[a-z]{3}\d{5}\.h", i) and len(i) == 10:
            try:
                metid = helper.getmetid(path_to_gen)
            except:
                metid = None
            tasks.append((i.split('.')[0],metid))
            try:
                testgen(path_to_gen)
            except:
                settings.log.writeln("произошла ошибка при проверке " + i)
        else:
            settings.log.writeln(i+" проигнорировано")
    return tasks

def start(path_to_arx, prog):
    settings.default_init()
    try:
        cleandir(settings.path_to_gens)
    except:
        raise RuntimeError("Ошибка очистки директории")
    settings.log.cleandata()
    unrar(path_to_arx, prog)
    tasks = test()
    return settings.log.data(), tasks