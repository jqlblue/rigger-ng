#coding=utf-8

import interface
from utls.rg_io  import rg_logger,rgio
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from string import *
from utls.rg_utls import check_proc
import os,re,setting
from php import php,python

#守护进程的基类
class daemon_base(interface.resource,interface.base):

    def _before(self,context):
        self.zdaemon    = value_of(self.bin)
        self.script     = value_of(self.script)
        self.logpath    = value_of(self.logpath)
        self.runpath    = value_of(self.runpath)
        self.worker     = int(value_of(self.worker))
        if not self.__dict__.has_key("main_ukey"):
            import hashlib
            self.main_ukey  = hashlib.md5(self.script +self.runpath ).hexdigest()
        self.ukeys      = {}
        self.confs      = {}

        for i in range(1,self.worker + 1 ):
            self.confs[i]       = self.runpath +  "/zdaemon-%d-%s.xml" %(i, self.main_ukey)
            self.ukeys[i]       = "%s_%d" %(self.main_ukey,i)
        self.program    = self.script

    def _config(self,context):
        for i in range(1,self.worker + 1):
            self.build_conf(self.ukeys[i],self.confs[i])

    #构建daemon的配置文件
    def build_conf(self,ukey,conf):
        content = """
<runner>
    program         $SCRIPT
    backoff-limit   10
    daemon          $DAEMON
    forever         $FOREVER
    exit-codes      0,2
    umask           022
    directory       .
    default-to-interactive True
    hang-around     False
    transcript      $LOG/zout.log.$UK
    socket-name     $RUN_PATH/$UK.sock
</runner>

<eventlog>
    level info
    <logfile>
    path $LOG/zrun.log.$UK
    </logfile>
</eventlog>

<environment>
 $ENVS
</environment>
"""
        envstr = ""
        if  not ( "hostname" in os.environ    or "HOSTNAME" in os.environ ) :
            import socket
            host = socket.gethostname()
            os.environ['hostname'] = host
        for k,v in os.environ.items():
            if k  == "PS1" :
                continue
            v = v.strip()
            #对于环境变量过滤非法字符
            if not re.search(r"[\$\n<>]",v):
                envstr = envstr + "\t%s %s \n" %(k.upper() , v)

        #在setting中配置输入日志
        logpath = setting.log_root + "/" + self.logpath
        c = Template(content).substitute(SCRIPT=self.program, DAEMON=self.daemon,FOREVER=self.forever,LOG=logpath,UK=ukey,RUN_PATH=self.runpath,ENVS=envstr)
        rg_logger.info("zdemon conf:")
        rg_logger.info(c)
        if not os.path.exists(logpath) :
            shexec.execmd(" mkdir -p " + logpath)
        with  open(conf ,'w') as f :
            f.write(c)


    # def depend(self,m,context):
    #     if "python" == python.bin : # fullpath /usr/local/bin/python
    #         m.check_exists("/usr/local/bin/" + python.bin)
    #     else :
    #         m.check_exists(get_env_conf().python)
    #     m.check_exists(self.zdaemon)

    def _start(self,context):
        cmd_tpl = "$PYTHON  $ZDAEMON  -C $CONF  start "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd  = Template(cmd_tpl).substitute(PYTHON=python.bin ,ZDAEMON = self.zdaemon,CONF= conf)
            print cmd

            print ("start: " + self.program)
            shexec.execmd(cmd)

    def _stop(self,context):
        cmd_tpl = "$PYTHON  $ZDAEMON  -C $CONF  stop "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd  = Template(cmd_tpl).substitute(PYTHON=python.bin ,ZDAEMON = self.zdaemon,CONF= conf)
            shexec.execmd(cmd)


    def _check(self,context):
        cmd_tpl = "ps auxww | grep zdaemon | grep  $CONF  | grep -v 'grep' "
        for i in range(1,self.worker + 1):
            conf = self.confs[i]
            cmd     = Template(cmd_tpl).substitute(CONF= os.path.basename(conf))
        check_proc("zdaemon",cmd)
#       program 太长。。。
        print ("program:" +  self.program)
        main_cmd =  ""
        for sub in self.program.split(' '):
            if len(sub) > len(main_cmd):
                main_cmd = sub
        cmd = Template("""ps auxww | grep -v "grep" | grep "$PROG" """).substitute(PROG= main_cmd )
        check_proc("daemon_prog ",cmd)

#用于 在守护经常中执行一般的shell脚本
#不需要额外的资源
class daemon (daemon_base):
    """
    示例:
    !R.daemon:
        script : "${PRJ_ROOT}/src/apps/console/work.sh"
    """
    script   = ""
    daemon   = "True"
    umask    = "022"
    forever  = "True"
    logpath  = "${PRJ_NAME}/"
    runpath  = "${RUN_PATH}"
    worker   = 1
    bin      = "/usr/local/bin/zdaemon"

#用于在守护进程中 php基本
#需要知道php的资源位置
class daemon_php(daemon_base):
    """
    示例:
    !R.daemon_php :
        script : "${PRJ_ROOT}/src/apps/console/work.php"
        php_ini: "${PRJ_ROOT}/conf/used/php.ini"
    """
    php_ini  = "${PHP_INI}"
    script   = ""
    daemon   = "True"
    umask    = "022"
    forever  = "True"
    logpath  = "${PRJ_NAME}/"
    runpath  = "${RUN_PATH}"
    worker   = 1
    bin      = "/usr/local/bin/zdaemon"


    def _allow(self,context) :
        return True

    #在执行前初始化php的资源路径
    def _before(self,context):
        daemon_base._before(self,context)
        self.php_ini    = value_of(self.php_ini)
        self.program    = "%s -c %s -f %s " %(php.bin,self.php_ini,self.script)


    def _info(self,context):
        rgio.struct_out("daemon: %s" %(self.program))
