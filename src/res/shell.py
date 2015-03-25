#coding=utf-8
import interface
import os,sys,getopt

from utls.rg_var import value_of
from string import *
from utls.rg_sh  import shexec

from   utls.rg_io import rgio

#execute shell script in conf file
#执行shell脚本
#用于项目初始化的配置和其他功能
class shell(interface.resource):

    """
      - !R.shell
           script: "${PRJ_ROOT}/data/init.sh"
    """
    script = ""

    def exec_script(self,args):
        if os.path.exists(self.script) :
            cmd = self.script  +  " " + args
            shexec.execmd(cmd,True)

    def _allow(self,context) :
        return True

    def _before(self,context):
        self.script = value_of(self.script)

    def _config(self,context):
        self.exec_script("config")

    def _start(self,context):
        self.exec_script("start")

    def _stop(self,context):
        self.exec_script("stop")

    def _data(self,context):
        self.exec_script("data")

    def shell(self,context):
        self.exec_script("shell")

    def _reload(self,context):
        self.exec_script("reload")

    def _clean(self,context):
        self.exec_script("clean")

    def _check(self,context):
        exists = os.path.exists(self.script)
        self._check_print(exists,self.script)
        self.exec_script("check")

    def _info(self,context):
        rgio.struct_out("script: %s" %(self.script))
        return self.script

    def depend(self,m,context):
        m.check_exists(self.script)


##
# @brief 直接运行shell指令
class dx_shell(interface.resource):

#     def __init__(self,env,script):
# #        self.env = env
#         self.script = script
    def _before(self,context):
#        self.env.locate()
        self.script = value_of(self.script)
    def shell(self,context):
        cmd = self.script
        shexec.execmd(cmd)

    def _info(self,context):
        rgio.struct_out("cmd: %s" %(self.script))
        return self.script
