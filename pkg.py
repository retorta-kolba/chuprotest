import rarfile
import os

if __name__ != '__main__':
    import chuprotest.settings
    settings = chuprotest.settings

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
        prog_pass = password("psa")
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

def test():
    pass
    
def start(path_to_arx, prog):
    try:
        cleandir(settings.path_to_gens)
    except:
        raise RuntimeError("Ошибка очистки директории")
    settings.log.cleandata()
    unrar(path_to_arx, prog)
    