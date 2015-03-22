#coding=utf8
import types , re , os , string ,  getopt , pickle ,yaml
import setting
from utls.rg_io import rgio ,rg_logger
import logging


#存储rg参数的实体
class rg_args :
    def __init__(self):
        self.conf          = os.getcwd() + "/_rg/conf.yaml"
        self.log_level     = logging.ERROR
        self.os            = None
        self.user          = None
        self.root          = os.path.dirname(os.path.realpath(__file__))
        self.root          = os.path.dirname(self.root)

    def clear(self):
        pass

#存储项目参数的实体
class prj_args :
    def __init__(self):
        #环境 包含env demo online等
        self.env  = None
        #配置的参数
        self.conf = None
        #系统 front admin等
        self.sys  = None
        #指令集
        self.cmds = []

    def clear(self):
        self.cmds = []

    def __str__(self) :
        cmd = "," . join(self.cmds)
        return "%s -e %s -s %s" %(cmd,self.env,self.sys)


#运行时的参数实体
class run_args :
    def __init__(self):
        self.rg  = rg_args()
        self.prj = prj_args()

    def clear(self):
        self.rg.clear()
        self.prj.clear()

    def parse_cmd(self):
        if len(self.cmds) == 0 :
            raise badargs_exception("æ²¡æå½ä»¤")
        if len(self.cmds) > 1:
            self.subcmd = self.cmds[1:]
            rg_logger.info("subcmd: %s" %self.subcmd)
        cmdarr = self.cmds[0].split(',')
        return cmdarr

    #加载 上一次参数实体
    @staticmethod
    def load(data_file):
        rargs     = run_args()
        if os.path.exists(data_file):
            try:
                with open(data_file,'r')  as f:
                    rargs = pickle.load(f)
            except Exception as  e :
                rgio.prompt("load rigger file fail!")
        #清空实体
        rargs.clear()
        return rargs

    #将本对象系列化到配置文件中
    def save(self,data_file):
        with open(data_file,'w')  as f:
            pickle.dump(self, f)

    #更新实体的参数
    def parse_update(self,parser) :
        self.argv          = parser.argv
        self.prj.cmds = parser.cmds
        if self.argv.has_key('-c') :
            self.prj.conf  = self.argv['-c']
        if self.argv.has_key('-z'):
            self.rg.user  = self.argv['-z']
        if self.argv.has_key('-e'):
            self.prj.env  = self.argv['-e']
        if self.argv.has_key('-o'):
            self.rg.os    = self.argv['-o']
        if self.argv.has_key('-s'):
            self.prj.sys = self.argv['-s']


    def __str__(self):
        info = str(self.prj)
        return  info
    @staticmethod
    def help():
        # rgio.prompt("rg  <dev cmd>   [-m <message>] ")
        rgio.prompt("rg  <svc cmd> [-e <env>] [-s <system>] [-c <prj.yaml>]")
        # rgio.prompt("rg  <svc cmd>   [-e <env>]     [-s <system>]   [-x <resource>]  [-f <script>]    [-v <vardef>]")
        # rgio.prompt("rg  <pub cmd>   [-p <project>] [-l <publish plan> ]  [-h [@|%]<host>] [-t [@]<tag>] [-z <rguser> ]")
        # rgio.prompt("rg  <batch cmd> [-p <project>] [-l <publish plan> ]  [-h [@|%]<host>] [-t [@]<tag>] [-z <rguser> ]")
        rgio.prompt("\ncommon args : [-d <level> ]\n")


class rarg_parser:

    ST_NEXT     = 0
    ST_CMD      = 1
    ST_ARG_KEY  = 3
    ST_ARG_VAL  = 4

    def __init__(self):
        self.argv  = {}
        self.cmds  = []

    def load_args(self,saved ) :
        if hasattr(saved,'vars_def') and saved.vars_def is not None:
            if not self.argv.has_key('-v') :
                self.argv['-v'] = saved.vars_def
            else:
                rg_logger.info ( "old prior vars ignore:  %s " % rargs.vars_def)


    #解析用户输入的参数
    def parse(self,argv):

        self.__init__()
        status = self.ST_NEXT
        key    = ""
        val    = None
        for item in argv :
            item = item.strip()
            while True:
                if status == self.ST_ARG_VAL:
                    #正则分析指令
                    if re.match(r'-\w+',item) :
                        status  = self.ST_NEXT
                        continue
                    val = item
                    self.argv[key] = val
                    status  = self.ST_NEXT
                    break;
                if status == self.ST_ARG_KEY:
                    key = item
                    status = self.ST_ARG_VAL
                    break;
                if status == self.ST_CMD:
                    if len(item.strip()) > 0:
                        self.cmds.append(item)
                    status  = self.ST_NEXT
                    break;
                if status == self.ST_NEXT :
                    if re.match(r'-\w\S+',item) :
                        key = item[0:2]
                        val = item[2:]
                        self.argv[key] = val
                        status  = self.ST_NEXT
                        break;
                    elif re.match(r'-\w',item) :
                        status = self.ST_ARG_KEY
                    else :
                        status = self.ST_CMD
