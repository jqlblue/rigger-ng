#coding=utf-8
import interface
import os

from utls.rg_var import value_of
from string import *
from utls.rg_sh  import shexec
from utls.rg_io import rgio
from utls.rg_utls import get_rg_home
from php import php,python


class memcached(interface.resource):

    """
     - !R.memcached
          ip: "127.0.0.1"
          bin: "/usr/local/bin/memcached"

    """

    ip        = "127.0.0.1"
    port      = "11211"
    mem       = "32"
    bin       = "/usr/local/bin/memcached"
    def _before(self,context):
        self.port    = env_exp.value(self.port)
        self.ip      = env_exp.value(self.ip)
        self.mem     = env_exp.value(self.mem)
        prj_key      = env_exp.value("${PRJ_KEY}")
        self.pid     = rg_run_path() +  "/memcached_" + prj_key +"_" + self.port + ".pid"
    def start(self,context):
        cmdtpl="$MEMCACHED -d -m $MEM -u root -l $IP  -p$PORT -P $PID"
        cmd = Template(cmdtpl).substitute( MEMCACHED=self.bin,IP=self.ip,PORT= self.port, PID=self.pid, MEM=self.mem)
        rg_sh.shexec.execmd(cmd)
    def stop(self,context):
        if get_key("是否确定停止 Memcached ? (y/N)" , context)  == "y" :
            stop_service("Memcached",self.pid)
    def reload(self,context):
        print("reload memcached is ignore! ")
    def check(self,context):
        cmdtpl = "ps auxww | grep memcached | grep  $PORT  "
        cmd = Template(cmdtpl).substitute(PORT=self.port)
        check_proc("Memcached",cmd)

    def _info(self,context):
        rgio.struct_out("memcached ip: %s" %(self.ip))
        rgio.struct_out("memcached port: %s" %g(self.prot))
        rgio.struct_out("memcached mem: %s M" ))
