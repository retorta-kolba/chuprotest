import clang.cindex
import re
import __main__
# dict_list
dict_list = {}
warning = list()

class Block:
    children = list()
    childrenNode = list()
    node = None
    vidSet = set()
    def __init__(self, node, vids):
        self.vidSet = vids
        self.children = list()
        self.childrenNode = list()
        self.node = node     
        self.find_if(node)
    def find_if(self, node):
        kind = None
        try:
            kind = node.kind
        except:
            pass
            return 1
        if node.kind == clang.cindex.CursorKind.IF_STMT:
            self.children.append(If(node, self.vidSet))
            self.childrenNode.append(node)
            return 0
        else:
            for i in node.get_children():
                self.find_if(i)


    def get_children(self):
        return self.children
    def __str__(self):
        ret = "{"
        if len(self.get_children()) > 0:
            ret += str(self.get_children()[0])
            for i in self.get_children()[1:]:
                ret += ';\n' + str(i) 
        return ret + "}"        
        
class If:
    """
    """
    BlockIf = None
    BlockIfNode = None
    BlockElse = None
    BlockElseNode = None
    vidSet = None
    location = []
    #cond = None
    def __init__(self, node, vids):
        self.vidSet = vids
        assert node.kind == clang.cindex.CursorKind.IF_STMT
        self.location = (node.location.line, node.location.column)
        children = list(node.get_children())
        self.cond = get_cond(node)
        self.eval_cond()
        assert len(children) == 2 or len(children)==3
        self.BlockIf = Block(children[1], self.accept)
        self.BlockIfNode = children[1]
        if len(children) == 3:
            # no else
            self.BlockElse = Block(children[2], self.reject)
            self.BlockElseNode = children[2]

    def get_BlockIf(self):
        return self.BlockIf
    
    def eval_cond(self):
        global vid, warning
        if len(self.vidSet) == 0:
            empty = True
        else:
            empty = False
        accept = set()
        parseFail = False
        always_True = True
        always_False = True
        for i in self.vidSet:
            vid = i
            try:
                #print(i, eval(self.cond))
                #print(locals(), globals())
                if eval(self.cond, None, {}):
                    accept.add(i)
                    always_False = False
                else:
                    always_True = False
            except:
                parseFail = True
                accept = set(self.vidSet)
                reject = set(self.vidSet)
                always_True = False
                always_False = False
                break
        if not empty:
            if always_True:
                warning.append(str(self.location[0]-line_shift) + ' ' + self.cond + " always True")
            if always_False:
                warning.append(str(self.location[0]-line_shift) + ' ' + self.cond + " always False")
        self.accept = accept
        if parseFail:
            self.reject = reject
        else:
            self.reject = self.vidSet - accept 
        ####
        #print(self.cond, self.accept, self.reject)
        ####
    
    def get_BlockElse(self):
        return self.BlockElse
    
    def __str__(self):
        ret = "if"+self.cond
        if self.BlockIf is not None:
            ret +=str(self.get_BlockIf())
        if self.BlockElse is not None:
            ret +="else" + str(self.get_BlockElse())      
        return ret

def vidin(vidlist):
    if vidlist not in dict_list:
        return False
    else:
        for i in dict_list[vidlist]:
            if vid == i:
                return True
    return False
    
def get_cond(precond):
    res = str()
    open_brackets = 0
    prev_vidin = False
    in_vidin = False
    open_vidin_brackets = 0
    for i in list(precond.get_tokens())[1:]:
        tmp = i.spelling.decode("cp1251")
        if tmp == '(':
            open_brackets += 1
            if in_vidin:
                open_vidin_brackets += 1
        if tmp == ')':
            open_brackets -= 1
            if in_vidin:
                open_vidin_brackets -= 1
        if tmp == "vidin":
            prev_vidin = True
            in_vidin = True
        assert open_brackets >= 0
        # add
        if tmp == "&&":
            res += " and "
        elif tmp == "||":
            res += " or "
        elif tmp == "!":
            res += " not "
        elif tmp == '/':
            res += "//"
        elif tmp == "(" and prev_vidin:
            prev_vidin = False
            res += "(\""
        elif tmp == ")" and in_vidin and open_vidin_brackets == 0:
            res += "\")"
            in_vidin = False
        else:
            res+=tmp
        if open_brackets == 0:
            break 
    return res

def parse_list(inputstr):
    global dict_list
    wspace = "(\s*)"
    word = "([a-zA-Z0-9_]+)"
    number = "(\d+)"
    ulist = "UINT8" + wspace + word + '\[' + wspace + "(\d*)" + wspace + ']' + wspace + '=' + wspace + '{' + wspace + '(' +word + wspace + '(,{0,1})' + wspace + ")*}" 
    # print(list(re.finditer(ulist, inputstr)))
    for i in re.finditer(ulist, inputstr):
        # print(i.group())
        name = i.group().split('[')[0].split()[-1]
        vids = set()
        for i in i.group().split('{')[1].split('}')[0].split(','):
            if len(i.strip()) > 0:
                vids.add(eval(i.strip()))
        # print(vids)
        #it`s not good
        #assert name not in dict_list
        dict_list[name] = vids

def vid_count(inputstr):
    wspace = "(\s*)"
    word = "([a-zA-Z0-9_]+)"
    number = "(\d+)"
    find = False
    enum1 = "enum" + wspace + "{" + "([^}]*)" + wspace + "vidov" + wspace + "}"
    enum2 = "vidov" + wspace + '=' + wspace + number 
    enum1_list = list(re.finditer(enum1, inputstr))
    enum2_list = list(re.finditer(enum2, inputstr))
    assert len(enum1_list) + len(enum2_list) <= 1
    # print(enum1_list)
    for i in enum2_list:
        #print(i.group())
        return int(i.group().split('=')[1])
    for i in enum1_list:
        vids = str()
        for j in i.group().split('{')[1].split('}')[0].split('\n'):
            vids += j.split('//')[0].strip()
        # print(vids)
        vids = vids.split(',')[:-1]
        # print(vids)
        for j in range(len(vids)):
            globals()[vids[j].strip()] = j
        return len(vids)
    return 1

def init_my_static():
    global path_to_gens, path_to_lib, path_to_texlib, path_to_pdfdir, log
    path_to_gens = __main__.path_to_gens
    path_to_lib = __main__.path_to_lib
    path_to_texlib = __main__.path_to_texlib
    path_to_pdfdir = __main__.path_to_pdfdir
    log = __main__.log    

def vid_analysis(generator):
    global line_shift, warning, dict_list
    index = clang.cindex.Index.create()
    dict_list.clear()
    warning.clear()
    filename = "tmpanalis.cpp"
    analysisfile = open("tmpanalis.cpp",'w',encoding='cp1251')
    analysisfile.write("//clang header\n")
    analysisfile.write("#define __GZ3__(a,b,c,d) int main()\n")
    analysisfile.write("//clang header\n")
    line_shift = 3
    inputstr = str()
    inputfile = open(path_to_gens+generator, 'r', encoding = 'cp1251')
    inputlist = list(inputfile)
    inputparse = index.parse(path_to_gens+generator)
    currentstr = 1
    need_close_brace = False
    need_open_brace = False
    prev_if = False
    in_if = False
    open_if_brackets = 0
    for i in inputparse.cursor.get_tokens():
        analysisfile.write('\n' * (i.location.line - currentstr))
        currentstr += (i.location.line - currentstr)
        tmp = i.spelling.decode("cp1251")
        if tmp == "if":
            prev_if = True
        elif prev_if and tmp == '(':
            in_if = True
            open_if_brackets = 1
            prev_if = False
        elif in_if and tmp == '(':
            open_if_brackets += 1
        elif in_if and tmp == ')':
            open_if_brackets -= 1
            
        #print(need_open_brace, tmp)    
        # write
        if need_open_brace:
            if tmp != '{' and tmp != "if":
                need_open_brace = False
                need_close_brace = True
                analysisfile.write("{ "+tmp)
            else:
                need_open_brace = False
                analysisfile.write(tmp)
        elif need_close_brace and tmp == ';':
            analysisfile.write(tmp+" }")
            need_close_brace = False 
        else:   
            analysisfile.write(tmp)
        
        analysisfile.write(' ')
        # after
        if open_if_brackets == 0 and in_if:
            need_open_brace = True
            in_if = False
    
    for i in inputlist:
        inputstr += i#.strip()
    analysisfile.close()
       
    
    tu = index.parse(filename)
    vids = vid_count(inputstr)
    #print(vids)
    parse_list(inputstr)
    # print(dict_list)
    a = Block(tu.cursor, set(range(vids)))
    #print(a)
    return len(warning) == 0, warning