import rarfile

if __name__ != '__main__':
    import chuprotest.settings
    settings = chuprotest.settings

# TODO: my_error
def password(prog):
    passfile = open(settings.path_to_pass,'r',encoding='cp1251')  # cp-1251?
    for i in passfile:
        if i.split('=')[0].strip() == prog:
            passfile.close()
            return i.split('=')[1].strip()
    else: 
        passfile.close()
        raise RuntimeError("Проблеы с паролем: пароль не найден.")

def unrar(path_to_arx, prog):
    prog_pass = password("psa")
    
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
        
