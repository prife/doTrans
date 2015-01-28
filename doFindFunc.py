#!//usr/bin/python

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

p_func = re.compile(r'(public|private)?\s*((\w+\s+)?\w+)\s*\(([^()]*)\)\s*{')
def parsefunction(txt, classname):
    pos = 0
    m = p_func.search(txt)
    if m is not None:
        txt_tmp = txt[m.end():]
        pos = getmatch(txt_tmp, '{', '}', 1)
        # ('','HandoverTransfer findHandoverTransfer', 'HandoverTransfer ', 'String sourceAddress, boolean incoming'), 
        if nextchar(txt_tmp, pos+1) == ';':
            pos = m.end()+pos+1
            print "######### here is anonymous class ###########"
        else:
            # here is an normal function!
            pos = m.end()+pos+1
            #func_content = txt[m.start():pos]
            m_prefix = m.group(1)
            m_ret_type = m.group(3)
            m_name = m.group(2)[len(m_ret_type):]
            m_args = m.group(4)
            func_content_cpp = m_ret_type + classname + "::" + m_name +'(' + m_args + ') {' + txt[m.end():pos]
            print func_content_cpp

    return pos

p_class = re.compile(r"(public|private)?\s*(static)?\s*(final)?\s*class\s*(\w+)\s*(extends\s+(\w+))?\s*(implements)?\s*([^{]*){")
def parsejava(txt):
    i = 0
    new_txt = ''
    iter_txt = txt
    while i < len(iter_txt):
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
        j = 0
        while j < len(class_txt):
            ret = parsefunction(class_txt, m_class_name)
            if ret == 0:
                break
            class_txt= class_txt[ret:]

parsejava(javatxt);

#
#l = re.findall(patten1, txt, re.S)
#lines = [i[:-1] for i in l]
#
#new_txt = ';\n'.join(lines)
#
#fout = open(fname, 'w')
#fout.write(new_txt)
