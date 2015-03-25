#coding=utf-8
import interface
import os,sys,getopt

from utls.rg_var import value_of
from string import *
from utls.rg_sh  import shexec
from   utls.rg_io import rgio

from php import php,python


#unix的定时任务
class crontab(interface.resource):
    """
     - !R.crontab
          cron: "${PRJ_ROOT}/conf/used/crontab.cron"

    """
    key   = "${PRJ_NAME}_${APP_SYS}"
    cron  = None
    def _before(self,context):
        self.cron   = value_of(self.cron)
        self.key    = value_of(self.key)
        user        = value_of("${USER}")
        self.tmp_cron    = "/tmp/" + user + "_"  + self.key + ".cron"
    def _start(self,context):
        self.append_conf(context)

    def _stop(self,context):
        self.clean_conf(context)

    def _info(self,context):
        rgio.struct_out("crontab")
        rgio.struct_out("cron: %s" %(self.cron),1)

    def append_conf(self,context):
        if not os.path.exists(self.cron):
            raise error.rigger_exception("cron file not exists : %s" %self.cron)
        cmdtpl= """
crontab -l >  $ORI_CRON ;
$PYTHON $CURPATH/sysconf.py  -n $KEY -f $ORI_CRON -t '#' -c $CRON -p file ;
crontab $ORI_CRON
"""
        #指定要运行文件sysconf的路径
        path =  os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../'),'utls')
        c = Template(cmdtpl).substitute(PYTHON=python.bin,CURPATH=path,KEY=self.key, ORI_CRON=self.tmp_cron,CRON=self.cron)
        shexec.execmd(c,True)

    def clean_conf(self,context):
        cmdtpl= """
crontab -l >  $ORI_CRON ;
$PYTHON $CURPATH/sysconf.py  -n $KEY -f $ORI_CRON -t '#' -c ''  ;
crontab $ORI_CRON
"""
        #指定要运行文件sysconf的路径
        path =  os.path.join(os.path.abspath(os.path.dirname(__file__) + '/../'),'utls')
        c       = Template(cmdtpl).substitute(PYTHON=python.bin,CURPATH=path,KEY=self.key,ORI_CRON=self.tmp_cron,CRON=self.cron)
        # print c
        shexec.execmd(c,True)
    pass
