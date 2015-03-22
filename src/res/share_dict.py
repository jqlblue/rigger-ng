#coding=utf-8
import interface
import os,sys,getopt

from utls.rg_var import value_of
from string import *

from   utls.rg_io import rgio
sys.path.append('/usr/local/lib')
from  pylon2py import *

class share_dict(interface.resource):

    """
      - !R.shared_dict
            pylon 共享dict的使用
            name: 共享dict的KEY, 避免冲突
            size: dict 大小(单位M)
            file: 加载的文件key:value
    """

    name       = "pylon_sdict"
    size       = "10"
    file       = ""

    def _allow(self,context) :
        return True

    def _before(self,context):
        self.name  =  value_of(self.name)
        self.size  =  int(value_of(self.size))
        self.file  =  value_of(self.file)
        pylon_sdict_create(self.name,self.size,1,1)

    def _data(self,context):
        pylon_sdict_data(self.file,"","")

    def _clean(self,context):
        pylon_sdict_remove(self.name)

    def find(self,context):
        key = context.rargs.argv['-k']
        key = value_of(key)
        print pylon_sdict_find(key)
        return pylon_sdict_find(key)
        pass

    def _info(self,context):
        rgio.struct_out("pylon_sdict name: %s" %(self.name))
        rgio.struct_out("pylon_sdict size: %s M" %(self.size))

# def help():
#     print( "bad args!")
#     print( "ag: sdict.py -c load -f a.txt -n test_space -s 1 ")
#
#
# if __name__ == '__main__':
#     #  sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#     # opts, args = getopt.getopt(sys.argv[1:], "c:f:n:s:k:", ["cmd=","files=","name=","size=","key="])
#     data_file   = None
#     space_size  = 1
#     space_name  = None
#     query_key   = ""
#     cmd = None
#     for o, a in opts:
#         if o == "-f":
#             data_file  = a
#         if o == "-c":
#             cmd = a
#         if o == "-s":
#             space_size = int(a)
#         if o == "-n":
#             space_name = a
#         if o == "-k":
#             query_key = a
#     if space_name is None  or   cmd is None:
#         help()
#         exit()
#     sdict = share_dict(space_name,space_size)
#     if cmd == "load" :
#         if data_file is None :
#             sdict.load(data_file)
#     if cmd == "clean":
#         sdict.clean()
#     if cmd == "find":
#         print (sdict.find(query_key))
#     pass
