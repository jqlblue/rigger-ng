#coding=utf-8
import interface
import os

from utls.rg_var import value_of
from string import *
from utls.rg_sh  import shexec
from utls.rg_io import rgio
from utls.rg_utls import get_rg_home
from php import php,python


#unix的系统日志
#默认采用syslog-ng
class syslog(interface.resource):
    """
     - !R.syslog
          conf: "${PRJ_ROOT}/conf/syslog.conf"
          bin: "/usr/local/syslog-ng"

    """
    append= None
    #syslog的默认配置文件
    conf  = "/etc/syslog.conf"
    key   = "${PRJ_NAME}"
    #依赖的系统路径
    #默认是centos安装的默认路径
    bin   = "/usr/local/bin/syslog-ng"

    def _before(self,context):
        self.conf     =  value_of(self.conf)
        self.append   =  value_of(self.append)
        self.prj_name =  value_of(self.key)
        self.bin      =  value_of(self.bin)

    def build_conf(self,context):

        #运行sysconf文件
        #指定路径
        path    =  os.path.join(get_rg_home() ,"utls")
        cmdtpl="$PYTHON $PATH/sysconf.py  -n $NAME -f $CONF -t '#' -c '$APPEND' -p file "
        c = Template(cmdtpl).substitute(PYTHON=python.bin,PATH=path,NAME=self.prj_name,APPEND=self.append,CONF=self.conf)
        shexec.execmd(c,True)

    def _clean(self,context):
        path    =  os.path.join(get_rg_home() ,"utls")
        cmdtpl="$PYTHON $PATH/sysconf.py  -n $NAME -f $CONF -t '#' -c '' "
        c = Template(cmdtpl).substitute(PYTHON=python.bin,PATH=path,NAME=self.prj_name,CONF=self.conf)
        shexec.execmd(c)
        self._reload(context)

    def _start(self,context):
        self.build_conf(context)
        self._reload(context)

    def _stop(self,context):
        self._clean(context)

    def _reload(self,context):
        cmdtpl ="$SYSLOG_CTRL reload"
        c = Template(cmdtpl).substitute(SYSLOG_CTRL=self.bin)
        shexec.execmd(c,True)

    def _info(self,context):
        rgio.struct_out("syslog: %s" %(self.conf))
