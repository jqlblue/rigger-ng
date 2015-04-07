from string  import Template
from utls.rg_sh  import shexec
import os


def check_proc(svc, found_cmd,expect_cn="1"):
    init=Template("V='-[ ]';SNAME=$NAME;PCNT=`$FOUND -c `; PCMD='$FOUND'; ").substitute(NAME=svc,FOUND=found_cmd)
    rev=  init +  "if test $PCNT -ge " + expect_cn + "; then V='-[Y]'; fi ;"
    cmd=  rev  +  """printf "%-100.90s%-20.20s%s\n" "$PCMD" "$SNAME($PCNT)" "$V" """
    shexec.execmd(cmd)

def get_rg_home():
    return os.path.abspath(os.path.dirname(__file__) + '/../')
