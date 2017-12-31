# grepsel #

## Why this wrapper
grepsel: gnu grep with select feature in recursive 
there already have the great ag, ack, grin, rak in the world fast vs faster
but which still not enough for me I'm start from turbo grep then semware grep 
some output style I'm prefer and cross the different text editor and section

grepsel act as wrapper for grep provide programmer searching for different source code via the command line
grepsel can use original vgrep script for vim, emacs, fte ...

grepsel support two output store in ~/legrep.grp for recall
grepsel.vim grepsel in vim script

###How to Use:###
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

###Add to .bashrc###
    function vg()
    {
    if [[ $1 == "?" || $1 == "--help" ]]; then
      echo "vg         ag viewer " 
      echo "   [regex] search for pattern via ag"
      echo "   [0..9]  for vim"

      return
    fi

    if [[ $1 == "" ]]; then
        grepsel -vv 0
        return
    fi

    re='^[0-9]+$'
    if [[ $1 =~ $re ]] ; then
           echo "Number !!!!"
           grepsel -vv $1
           return
    fi

    if [[ $1 == "-s" ]]; then
      grepsel -v
      return
    fi


    ag --fte $@ > ~/fte.grp
    grepsel -vv $@
    }
###Sample
	$ grepsel -py grepsel
	grepsel in progress....via gnu grep !!
	find . -name '*.py'
	[  1] ./grepsel/grepsel.py +2 """  grepsel power by lecheel 2o13  """
	[  2] ./grepsel/grepsel.py +285     print "grepsel in progress....via \033[1;91mGNU\033[0m grep !!"
	[  3] ./grepsel/grepsel.py +292     parser = ArgumentParser(description='grepsel using GNU grep wrapper for file(s).', add_help=False)
	[  4] ./grepsel/grepsel.py +299     parser.add_argument('-v','--vgrep',  action='store_true', help='grepsel gnu view and select for vim')
	[  5] ./grepsel/grepsel.py +300     parser.add_argument('-w','--wide',  action='store_true', help='grepsel wide view and select for vim')
	Prompt :2
        
        after choice 2 which launch vim automatically 
        
        $ grepsel 
        recall the last grep result prompt again

        $ grepsel 5
        launch vim for select line which cross the section

###Problem
        now grepsel [num] as quick launch how to grep real number [TODO]

![Screenshot](./grepsel.gif)
