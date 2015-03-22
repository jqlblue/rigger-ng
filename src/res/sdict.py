#coding=utf8
import os,sys,getopt
# from base     import *

sys.path.append('/usr/local/lib')
from pylon2py import *

class pylon_sdict:
    def __init__(self,name,size):
        self.name=name
        self.size=size
        pylon_sdict_create(name,size,1,1)
    def load(self,file):
        pylon_sdict_data(file,"","")
    def clean(self):
        pylon_sdict_remove(self.name)
    def find(self,key):
        return pylon_sdict_find(key)

def help():
    print( "bad args!")
    print( "ag: sdict.py -c load -f a.txt -n test_space -s 1 ")

if __name__ == '__main__':
    # sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    opts, args = getopt.getopt(sys.argv[1:], "c:f:n:s:k:", ["cmd=","files=","name=","size=","key="])
    data_file   = None
    space_size  = 1
    space_name  = None
    query_key   = ""
    cmd = None
    for o, a in opts:
        if o == "-f":
            data_file  = a
        if o == "-c":
            cmd = a
        if o == "-s":
            space_size = int(a)
        if o == "-n":
            space_name = a
        if o == "-k":
            query_key = a
    if space_name is None  or   cmd is None:
        help()
        exit()
    sdict = pylon_sdict(space_name,space_size)
    print sdict
    print sys.path
    if cmd == "load" :
        if data_file is None :
            help()
            exit()
        sdict.load(data_file)
    if cmd == "clean":
        sdict.clean()
    if cmd == "find":
        print (sdict.find(query_key))
    pass
