# grepsel #

## Why this wrapper
grepsel: gnu grep with select feature in recursive

grepsel act as wrapper for grep provide programmer searching for different source code via the command line
grepsel can use original vgrep script for vim, emacs, fte ...

grepsel support two output store in ~/legrep also the vgrep ~/fte.grp for recall

##How to Use:
usage: grepsel [--help] [-cc] [-mk] [-py] [-ja] [-v] [-w]
               [PATTERN [PATTERN ...]]
               
grepsel using GNU grep wrapper for file(s).
               
positional arguments:
PATTERN      the pattern to find
                 
optional arguments:
   --help       show this help message and exit
   -cc          search for all c and cpp [default]
   -mk          search for android mk and Makefile
   -py          search for py
   -ja, --java  search for java
   -v, --vgrep  grepsel gnu view and select for vim
   -w, --wide   grepsel wide view and select for vim


