#coding=utf8
from utls.rg_io import rgio , rg_logger
from rg_cmd_base import  rg_cmd , cmdtag_rg , cmdtag_prj ,cmdtag_pub
import utls.rg_var , interface
import res
from utls.rg_sh  import shexec
import os
from string import *

class prj_cmd_base :


    #初始化输入的环境-e env和系统-s sys
    #rargs 是默认参数 argv是输入参数
    def _config(self,argv,rargs):
        self.env = []
        if argv.has_key('-e') :
            self.env = argv['-e'].split(',')
        if rargs.prj.env :
            self.env = rargs.prj.env.split(',')

        self.sys = []
        if argv.has_key('-s') :
            self.sys = argv['-s'].split(',')
        if rargs.prj.sys:
            self.sys = rargs.prj.sys.split(',')


    #初步检查配置文件的属性和格式是否正确
    @staticmethod
    def check_data(data):
        if data is None :
            raise interface.rigger_exception('no project yaml data')
        if data.has_key('_env') and data.has_key('_prj') and data.has_key('_sys') :
            return True
        raise interface.rigger_exception('project data maybe no _env,_prj,or _sys')


    #指令执行器 rargs主要用于加载配置文件
    def runcmd(self,rargs,fun) :
        import impl.rg_yaml,copy
        #加载j解析配置文件
        loader = impl.rg_yaml.conf_loader(rargs.prj.conf)
        rg_logger.info("load prj conf: %s" %(rargs.prj.conf))
        data   = loader.load_data("!R","res")
        #初步检查配置文件的属性和格式是否正确
        prj_cmd_base.check_data(data)

        #获取inner.env对像集（多环境的配置文件）
        env_data    = data['_env']
        #获取inner.project对象
        prj_data    = data['_prj']
        #获取inner.systen对象集合（多系统的配置文件）
        sys_data    = data['_sys']


        #以下代码主要作用是将yaml文件中的
        #env prj sys 这3类信息放入main_prj 的父类control_box
        #的_res被作为一个内部资源的集合
        #res.prj_main在res.inner 中
        #同时作为一个资源递归调用的入口
        main  = res.prj_main()
        if len(self.env) == 0 :
            return

        #注册环境配置
        #查找输入的环境参数 对应在配置中yaml配置
        for env in self.env :
            for env_obj  in env_data :
                if env_obj._name == env :
                    main.append(env_obj)

        #注册项目配置
        #因为项目只有一个，所以不用查找
        main.append(prj_data)

        #注册系统配置
        #查找输入系统参数  对应在配置文件yaml配置
        if len(self.sys) > 0 :
            for sys in self.sys :
                for sysobj in   sys_data :
                    if  sysobj._name ==  sys :
                        main.append(sysobj)

        #运行时上下文对象
        context = interface.run_context()
        #解决自定义参数传递问题
        context.rargs = rargs

        #以aop的方式去链式的调用res资源
        #以递归的方式深度优先去遍历执行yaml文件中配置的资源
        interface.control_call(main,fun,context,"unknow")

class info_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg info
    """
    def _execute(self,rargs):
        rgio.struct_out("rg %s" %(rargs) )
        rgio.struct_out("")
        self.runcmd(rargs,lambda x , y : x._info(y))

class conf_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg conf -e <env> -s <sys> [-o <os>] "
    rg conf -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x , y : x._config(y))

class reconf_cmd(conf_cmd):
    """
    rg reconf
    """
    pass

class start_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg start -e <env> -s <sys> [-o <os>] "
    rg start -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._start(y))

class stop_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg stop -e <env> -s <sys> [-o <os>] "
    rg stop -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._stop(y))

class clean_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg clean -e <env> -s <sys> [-o <os>] "
    rg clean -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._clean(y))

class data_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg data -e <env> -s <sys> [-o <os>] "
    rg data -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._data(y))

class check_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg check -e <env> -s <sys> [-o <os>] "
    rg check -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._check(y))

class restart_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg restart -e <env> -s <sys> [-o <os>] "
    rg restart -e debug,demo -s front,admin
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x._stop(y))
        self.runcmd(rargs,lambda x,y : x._start(y))

class find_cmd(prj_cmd_base,cmdtag_prj):
    """
    rg find -k <key> -s <sys> [-o <os>] "
    """
    def _execute(self,rargs):

        self.runcmd(rargs,lambda x,y : x.find(y))

class shell_cmd(prj_cmd_base,cmdtag_prj):

    """
    rg shell  -e env -s <sys> [-o <os>] "
    """
    def _execute(self,rargs):
        self.runcmd(rargs,lambda x,y : x.shell(y))

class depend_cmd(prj_cmd_base,cmdtag_prj):

    """
    rg depend  -e env -s <sys> [-o <os>] "
    """
    def _execute(self,rargs):

        self.runcmd(rargs,lambda x,y : x.depend(y))


class init_cmd(prj_cmd_base,cmdtag_prj):
    """ 初始化环境 """
    def _execute(self,rargs):
        path=os.path.dirname(os.path.realpath(__file__))
        path=os.path.dirname(path)
        dst = os.getcwd() + "/_rg"
        # if os.path.exists(dst) :
        #     print(" _rg 已经存在！")
        #     return
        cmd = "~/devspace/rigger-ng/src/rg tpl $SRC -o $DST"
        cmd = Template(cmd).substitute(SRC=path + "/tpl" , DST=dst)
        # print cmd
        # exit()
        # shexec.execmd(cmd)
        cmd = """echo 'source ~/devspace/rigger-ng/rigger.rc' > $DST/_rigger.rc  """
        cmd = Template(cmd).substitute(DST=os.getcwd())
        print cmd
        # exit
        shexec.execmd(cmd)

class showconf_cmd(prj_cmd_base,cmdtag_prj):
    """
    查看当前配置
    """
    def _execute(sel,rargs):
        # prj_cmd_base._execute(self,cmd,rargs)
        rgio.simple_out(str(rargs))



# class (run_base,resconf_able,cmdtag_run):
#     """execut php eg: rg php -f 'xxx.php arg1 arg2'  """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         resconf_able._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-f":
#                 rargs.script = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         if  rargs.script is None or len(rargs.script)  == 0 :
#             raise error.rigger_exception(" need -f  argu")
#         dxphp   = resouce.dx_php(rargs.script.lstrip())
#         execmd  = lambda x,c :  call_shell(x,c)
#         self.runner.run_cmd(rargs,execmd,dxphp)
#
# class phpunit_cmd(run_base,resconf_able, cmdtag_run):
#     """execut php eg: rg phpunit -f '<your.xml> | <test path>'  """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         resconf_able._config(self,argv,rargs)
#         rargs.script = ""
#         for o, a in argv.items():
#             if o == "-f":
#                 rargs.script = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         punit = resouce.phpunit(rargs.script.lstrip())
#         execmd = lambda x,c :  call_shell(x,c)
#         self.runner.run_cmd(rargs,execmd,punit)
#
# class shell_cmd(run_base,resconf_able, cmdtag_run):
#     """execut shell eg: rg shell -f 'xxx.sh arg1 arg2' """
#     def _config(self,argv,rargs):
#         run_base._config(self,argv,rargs)
#         resconf_able._config(self,argv,rargs)
#         for o, a in argv.items():
#             if o == "-f":
#                 rargs.script = a
#     def _execute(self,cmd,rargs):
#         run_base._execute(self,cmd,rargs)
#         if rargs.script is None or len(rargs.script)  == 0 :
#             raise error.rigger_exception(" need -f  argu")
#         dxshell = resouce.dx_shell(vars(),rargs.script.lstrip())
#         execmd = lambda x,c :  call_shell(x,c)
#         self.runner.run_cmd(rargs,execmd,dxshell)
#     def _usage(self):
#         rgio.prompt('usage: shell -f <script>')
#         rgio.prompt('eg: rg shell -f "test/test_run.sh -a -b -c "')
