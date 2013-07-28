#! /usr/bin/python
"""  grepsel power by lecheel 2o13  """
""" gnu grep wrapper for programmer """
import string
import sys, os
import subprocess
import tempfile
from subprocess import call
from argparse import ArgumentParser, FileType

GREEN = '\033[32m'
RED = '\033[91m'
CYAN = '\033[36m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
PURPLE = '\033[35m'
PRETTY_GREEN = '\033[92m'
END_COLOR = '\033[0m'

def write_fnameline(fname,fline):
    f = open('/tmp/fname','w')
    curdir = os.getcwd()
    cmd="%s/%s \n" %(curdir,fname)
    f.write(cmd)
    f.close()
    f = open('/tmp/fline','w')
    f.write(fline)
    f.close()


def index_find(pattern, string, ignore_case):
    """Find index of pattern match in string. Returns -1 if not found."""
    if ignore_case:
        pattern = pattern.lower()
        string = string.lower()

    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

def color_find(pattern, string, ignore_case):
    """Find all matches of pattern in string. Returns colored string, or empty string if not found."""
    result = ''
    index = index_find(pattern, string, ignore_case)

    while index != -1:
        result += string[:index]
        result += RED + string[index:index + len(pattern)] + END_COLOR
        string = string[index + len(pattern):]
        index = index_find(pattern, string, ignore_case)

    return result if result == '' else result + string


def parse_hfile(fname):
    ret = 0
    if fname[0] == ".":
       idx=2
    else:
       idx=1
    try:
       h=fname.split(".")
       if len(h) == 2:
          if h[1] == "h":
              ret = 1
    except ValueError,IndexError:
       ret = 0
    return ret

def parse_vline(spat,sline,idx,lastname):
    fname=sline.split(":")[0]
    fline=sline.split(":")[1]
    hh=parse_hfile(fname)
    lastpos=len(fname)+len(fline)+2
    content=sline[lastpos:]
    str=color_find(spat,content,False)
    if str=="":
        str=content
#        print "[\033[1;35m%3s] \033[36m%s\033[0m +\033[1;33m%s\033[0m %s" % (idx+1, sline.split(":")[0],sline.split(":")[1],str)
    if lastname != fname:
        print "[\033[1;34m---\033[0m] \033[36mFile: %s\033[0m" % (sline.split(":")[0])
        print "[\033[1;35m%3s\033[0m] \033[1;33m%4s\033[0m %s" % (idx+1,sline.split(":")[1],content)
    else:
        print "[\033[1;35m%3s\033[0m] \033[1;33m%4s\033[0m %s" % (idx+1, sline.split(":")[1],str)


    return sline.split(":")[0]

def parse_v0line(spat,sline,idx,lastname):

    if sline[:4] == "File":
        fname=sline.split(":")[1]
        hh=parse_hfile(fname)
        if hh:
            print "[\033[1;34m%3s\033[0m] \033[36m%s\033[0m" % (idx+1,sline)
        else:
            print "[\033[1;34m%3s\033[0m] \033[92m%s\033[0m" % (idx+1,sline)
    else:
        fline=sline.split(":")[0]
        lastpos=len(fline)+2
        content=sline[lastpos:]
        str=color_find(spat,content,False)
        if str=="":
            str=content
        print "[\033[1;35m%3s\033[0m] \033[1;33m%4s\033[0m %s" % (idx+1, fline,str)

    return sline.split(":")[0]

def parse_line(spat,sline,idx):
#    print "parsing.... %s" %sline
    fname=sline.split(":")[0]
    fline=sline.split(":")[1]
    hh=parse_hfile(fname)
    lastpos=len(fname)+len(fline)+2
    content=sline[lastpos:]
    str=color_find(spat,content,False)
    if str=="":
        str=content
    if hh:
        print "[\033[1;35m%3s\033[0m] \033[36m%s\033[0m +\033[1;33m%s\033[0m %s" % (idx+1, sline.split(":")[0],sline.split(":")[1],str)
    else:
        print "[\033[1;35m%3s\033[0m] \033[92m%s\033[0m +\033[1;33m%s\033[0m %s" % (idx+1, sline.split(":")[0],sline.split(":")[1],str)


def parse_fnameline(sline,idx):
    lastpos=len(sline.split(":")[0])+len(sline.split(":")[1])+2
    content=sline[lastpos:]
    write_fnameline(sline.split(":")[0],sline.split(":")[1])
    fname = sline.split(":")[0]
    fline = "+%s" % sline.split(":")[1]
    EDITOR = os.environ.get('EDITOR','vim') #that easy!
    call([EDITOR, fname, fline])


def find_fname(idx):
    for i in range(idx,0,-1):
       if lines[i][:4] == "File":
           return i

def parse_vfnameline(sline,idx):
    EDITOR = os.environ.get('EDITOR','vim') #that easy!
    if sline[:4] == "File":
        fname = sline.split(":")[1][1:-1]
        call([EDITOR, fname])
    else:
        fline = sline.split(":")[0]
        ii=find_fname(idx)
        if ii>0:
           fname = lines[ii][6:][:-1]
           fline = "+%s" % fline.strip()
           call([EDITOR, fname, fline])
        else:
           print "Oops...!"

def prompt_choice(Max_choice,typ):
    myAns=raw_input("\033[32mPrompt \033[0m:")
    if myAns:
        try:
           idx=string.atoi(myAns)-1
           if idx < Max_choice-1:
               if typ == 1:
                  parse_fnameline(lines[idx],idx)
               else:
                  parse_vfnameline(lines[idx],idx)
           else:
               print "Out of range!"
        except ValueError:
           return
    else:
       print "Oops...!"

def color_print(spat,wideview):
    global lines
    home = os.path.expanduser("~")
    legrep = home+"/legrep"
    try:
      fp=open(legrep)
      lines = fp.readlines()
    except IOError:
      print "~legrep not Founded!!!"
      return
    else:
      fp.close()
    i=1;
    lastname="xxx"
    if len(lines)>100:
        print "Too big maintain here <\033[32m%s\033[0m> matches founded!!!" % len(lines)
        print "Try using following method:"
        print "find . -name .git -prune -o -type f \( \033[33m-name '*.mk' -o -name '*.c' -o -name '*.cc' -o -name '*.cpp' -o -name '*.h'\033[0m \) -print0 | xargs -0 grep --color -n %s" %spat
        cmd=raw_input("Press Enter to continue...")
        if not len(cmd):
            cmd = "less %s" % legrep
            os.system(cmd)
        return

    for line in lines:
        if wideview:
            lastname=parse_vline(spat,line[:-1],i-1,lastname)
        else:
            parse_line(spat,line[:-1],i-1)
        i=i+1
    if i>1:
        prompt_choice(len(lines),1)
    else:
        print "No Founed !!!!"
    return

"""
   real fte.grp wideview
   TODO

"""
def color_v0print(spat,wideview):
    global lines
    home = os.path.expanduser("~")
    legrep = home+"/fte.grp"
    fp=open(legrep)
    lines = fp.readlines()
    fp.close()
    i=1;
    lastname="xxx"
    if len(lines)>200:
        print "Too big maintain here <\033[32m%s\033[0m> matches founded!!!" % len(lines)
        print "Try using following method:"
        print "vgrep %s \*.c" %spat
        return
    print "\033[1;91mvGREP viewer\033[0m"
    for line in lines:
        lastname=parse_v0line(spat,line[:-1],i-1,lastname)
        i=i+1
    if i>1:
        prompt_choice(len(lines),0)
    else:
        print "No Founded !!!!"
    return

"""
    fte.grp in GNU style from fte.g__
    prase in GNU but show in wide

"""
def color_vprint(spat,wideview):
    global lines
    home = os.path.expanduser("~")
    legrep = home+"/fte.g__"
    fp=open(legrep)
    lines = fp.readlines()
    fp.close()
    i=1;
    lastname="xxx"
    if len(lines)>200:
        print "Too big maintain here <\033[32m%s\033[0m> matches founded!!!" % len(lines)
        print "Try using following method:"
        print "vgrep %s \*.c" %spat
        return
    print "\033[1;91mvGREP viewer\033[0m"
    for line in lines:
        if wideview:
            lastname=parse_vline(spat,line[:-1],i-1,lastname)
        else:
            parse_line(spat,line[:-1],i-1)
        i=i+1
    if i>1:
        prompt_choice(len(lines),1)
    else:
        print "No Founded !!!!"
    return

def gnu_grep(spat,use_cc,use_mk,use_py,use_java,wideview):
    if use_cc==True:
       gfiles="-name '*.mk' -o -name '*.c' -o -name '*.cc' -o -name '*.cpp' -o -name '*.h'"
    if use_mk==True:
       gfiles="-name '*.mk' -o -name 'Makefile' "
    if use_py==True:
       gfiles="-name '*.py'"
    if use_java==True:
       gfiles="-name '*.java'"

    cmd= "find . -name .repo -prune -o -name .git -prune -o -type f \( %s \) -print0 | xargs -0 grep --color -n '%s' > ~/legrep" %(gfiles,spat)
#    print cmd
    print "grepsel in progress....via \033[1;91mGNU\033[0m grep !!"
    print "  find . %s" % gfiles
    os.system(cmd)
    color_print(spat,wideview)


def setup_parser():
    parser = ArgumentParser(description='grepsel using GNU grep wrapper for file(s).', add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('pattern', metavar='PATTERN', nargs="*", help='the pattern to find')
    parser.add_argument('-cc', action='store_true', help='search for all c and cpp [\033[92mdefault\033[0m]')
    parser.add_argument('-mk', action='store_true', help='search for android mk and Makefile')
    parser.add_argument('-py', action='store_true', help='search for py')
    parser.add_argument('-ja','--java', action='store_true', help='search for java')
    parser.add_argument('-v','--vgrep',  action='store_true', help='grepsel gnu view and select for vim')
    parser.add_argument('-w','--wide',  action='store_true', help='grepsel wide view and select for vim')
    return parser

DEFAULT_PRINT_OPTIONS = (True, False, False, False, False)

def main():
    # set up argparse argument parser and get args
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern

    use_cc, use_mk, use_py, use_java, gview = DEFAULT_PRINT_OPTIONS

    grepview = False
    # default wideview or GNU view
    wideview = False

    if args.cc:
       use_cc = args.cc
    if args.wide:
       wideview = True

    if args.vgrep:
        color_v0print("vgrep",True)
        return

    if args.pattern:
        gnu_grep(pattern[0],use_cc,args.mk,args.py,args.java,wideview)
    else:
        try:
            spat = os.environ["spat"]
            print "Search Pattern: \033[31m%s\033[0m" %spat
        except KeyError:
            spat = ""
        color_print(spat,wideview)

if __name__ == '__main__':
    main()