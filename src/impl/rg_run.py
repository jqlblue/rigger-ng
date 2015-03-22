#coding=utf-8
import string , logging, sys
import interface, rg_args, rg_ioc
from utls.rg_io import rg_logger

def run_cmd(cmdstr,yaml_conf=None) :
    rargs  = rg_args.run_args()
    parser = rg_args.rarg_parser()
    parser.parse(cmdstr.split(' '))
    rargs.parse_update(parser)
    if yaml_conf is not None:
        rargs.prj.conf = yaml_conf

    run_rigger(rargs,parser.argv)


#实例化cmd对象
#执行父类prj_cmd_base的_config初始化输入的  环境env 和系统sys
#aop的方式执行相应的方法

def run_rigger(rargs, argv) :
    #TODO: muti cmd support
    if len(rargs.prj.cmds) == 0 :
        raise interface.rigger_exception("No Cmd!")
    cmds = rargs.prj.cmds[0]
    for  cmd in cmds.split(',') :
        obj = rg_ioc.ins_cmd(cmd)
        if obj is None :
            raise  interface.rigger_exception( "unfound '%s' cmd instance" %cmd)
        rg_logger.info("cmd: %s , cmd_ins : %s" %(cmd,obj.__class__.__name__))
        #初始化输入的环境-e env和系统-s sys
        #rargs 是是运行时参数对象
        #argv是输入参数
        obj._config(argv,rargs)
        obj._execute(rargs)




