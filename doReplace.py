#!/usr/bin/python

# encoding: UTF-8
import sys
import re

if len(sys.argv) >= 2:
    fsrc = sys.argv[1]
    fname = sys.argv[2]

fd = open(fsrc, 'rb+')
s = fd.read()

#add TAG
p=re.compile("String TAG = (\"\w+\")")
logtag = '''
#undef DEBUG_LEVEL
#define DEBUG_LEVEL 2
#undef LOG_TAG
#define LOG_TAG '''
m = p.search(s)
if m is not None:
    s = logtag + m.group(1) + '\n' + s

s = re.sub("\s*static final String TAG[^\n]*\n", "", s);
s = re.sub("\s*static final boolean DBG[^\n]*\n", "", s);
s = re.sub(r"\bboolean\b", "bool", s);
s = re.sub(r"\bint\b", "int32_t", s);

s = re.sub(r"\bfinal\b", "const", s);

s = re.sub(r"\bfinal\b", "const", s);
s = re.sub("byte\[\]", "sp<Blob<byte_t> >", s);
s = re.sub(r"\bString\b", "sp<String>", s);
s = re.sub(r"\bbyte\b", "byte_t", s);

to = r"\1//synchronized(\2) { \n\1{\n\1    GLOGAUTOMUTEX(alock, \2);"
s = re.sub("([ \t]*)synchronized[ \t]*\((\w+)\)[ \t]*{", to, s);

s = re.sub("(@Override)", "// @Override", s);

s = re.sub(r"\bnull\b", "NULL", s);

s = re.sub("Log\.d[ \t]*\(TAG, ", "GLOGD(", s);
s = re.sub("Log\.e[ \t]*\(TAG, ", "GLOGE(", s);
s = re.sub("Log\.i[ \t]*\(TAG, ", "GLOGI(", s);
s = re.sub("Log\.w[ \t]*\(TAG, ", "GLOGW(", s);
s = re.sub("Log\.v[ \t]*\(TAG, ", "GLOGV(", s);
s = re.sub("if \(DBG\)[ \t]*", "", s);

fout = open(fname, 'w')
fout.write(s)
