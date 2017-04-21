def getmetid(path):
    gen = open(path, 'r', encoding='cp1251')
    for i in gen:
        if '__GZ3__' in i:
            data = i.split('(')[1].split(')')[0].split(',')
            met = data[0].strip() + data[2].strip()[0] + data[1].strip()
            return met
    raise RuntimeError("metid not found")
