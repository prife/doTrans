#!/usr/bin/python

# encoding: UTF-8
import sys
import re

if len(sys.argv) >= 2:
    fsrc = sys.argv[1]
    #fname = sys.argv[2]

javatxt = open(fsrc, 'rb').read()

def getmatch(str, charopen, charclose, count = 0):
    i = 0;
    while i<len(str):
        if (str[i] == charopen):
            count = count + 1
        elif (str[i] == charclose):
            count = count - 1
        if (count == 0):
            break;
        i = i + 1;
    return i

def nextchar(txt, i):
    while i < len(txt):
        if txt[i] == '\n':
            i = i+1
        elif txt[i] == '\r':
            i = i+1
        elif txt[i] == '\t':
            i = i+1
        elif txt[i] == ' ':
            i = i+1
        else:
            return txt[i:i+1];
    return None

class CodeFunc():
    "function object"
    def __init__(self, prefix, ret_type, name, args, throws, body, classname=''):
        self.prefix = prefix;
        self.ret_type = ret_type;
        self.name = name
        self.args = args
        self.body = body
        self.classname = classname
        self.throws = throws

#p_func = re.compile(r'(public|private)?\s*((\w+\s+)?\w+)\s*\(([^()]*)\)([^{]*){')
#FIXME: does '\w' can be redefined?
jw=r"[a-zA-Z0-9_<>\[\].?]+"
jret_name=r"((" + jw + r"\s+)?" + jw + r")"
p_func = re.compile(r'(public|private)?\s*' + jret_name + r'\s*\(([^();]*)\)([^{;]*){')

def parsefunction(txt, classname):
    start = 0
    end = 0
    codefuc = None
    m = p_func.search(txt)
    if m is not None:
        txt_tmp = txt[m.end():]
        pos = getmatch(txt_tmp, '{', '}', 1)
        start = m.start()
        end = m.end()+pos+1
        if nextchar(txt_tmp, pos+1) == ';':
            # TODO: here is anonymous class
            pass
        else:
            # here is an normal function!
            # ('','HandoverTransfer findHandoverTransfer', 'HandoverTransfer ', 'String sourceAddress, boolean incoming'), 
            m_prefix = ''
            if m.group(1) is not None:
                m_prefix = m.group(1).strip()
            m_ret_type = ''
            if m.group(3) is not None:
                m_ret_type = m.group(3).strip()
            m_name = m.group(2)[len(m_ret_type):].strip()
            m_args = ''
            if m.group(4) is not None:
                m_args = m.group(4)

            m_throws = ''
            if m.group(5) is not None:
                m_throws = m.group(5)
            codefuc = CodeFunc(m_prefix, m_ret_type, m_name, m_args, m_throws, txt[m.end():end], classname)

    return (start, end, codefuc)

def parseClassFunction(txt, classname):
    funclist = []
    while True:
        start,end,codefunc = parsefunction(txt, classname)
        if end == 0:
            break
        funclist.append(codefunc)
        txt = txt[end:]
    return funclist

def createHeadFile(funclist):
    print "===============h==============="
    for f in funclist:
        if f is None:
            continue
        func = f.prefix + ' '+ f.ret_type + ' ' + f.name +'(' + f.args + ');'
        print func

def createCppFile(funclist):
    print "===============cpp============="
    for f in funclist:
        if f is None:
            continue
        func = f.prefix + ' '+ f.ret_type + ' ' + f.classname +'::' + f.name + \
               '(' + f.args + ') {' + f.body + ';'
        print func
        print

p_class = re.compile(r"(public|private)?\s*(static)?\s*(final)?\s*class\s*(\w+)\s*(extends\s+(\w+))?\s*(implements)?\s*([^{;]*){")
def parsejava(txt):
    new_txt = ''
    iter_txt = txt
    while True:
        m = p_class.search(iter_txt)
        if m is None:
            break;
        print "======== find class ========="
        print m.group(0)
        print "======== class end ========="

        m_class_name = m.group(4)
        m_pclass_name = m.group(6)
        m_class_interface = m.group(8)

        iter_txt_tmp = iter_txt[m.end():]
        pos = getmatch(iter_txt_tmp, '{', '}', 1)
        iter_txt = iter_txt_tmp[pos+1:] #skip '}'

        # produce class function name
        class_txt = iter_txt_tmp[:pos]
        funclist = parseClassFunction(class_txt, m_class_name)
        #print "funclist:", funclist
        createHeadFile(funclist)
        createCppFile(funclist)

parsejava(javatxt);

#
#l = re.findall(patten1, txt, re.S)
#lines = [i[:-1] for i in l]
#
#new_txt = ';\n'.join(lines)
#
#fout = open(fname, 'w')
#fout.write(new_txt)
