#coding=utf-8
import logging
import interface
import utls.rg_io

from utls.rg_io import rg_logger


#分别向容器注入资源和指令集
#可以再此处添加资源和指令
def setup() :

    #注册系统内部资源
    interface.regist_res("env,project,system,xmodule,prj_main" , "res.inner")
    interface.regist_res("echo,vars,assert_eq"                 , "res.inner")

   #注册扩展资源
    interface.regist_res("link,path,intertpl,file_tpl"         , "res.files")
    interface.regist_res("mysql"                               , "res.mysql")

    interface.regist_res("daemon,daemon_php"                               , "res.daemon")


   #注册系统指令
    interface.regist_cmd("check,clean,info,init"                    , "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("conf,reconf,start,stop,restart,data" , "impl.rg_cmd.rg_cmd_prj")
    interface.regist_cmd("help"                                , "impl.rg_cmd.rg_cmd")


    #注入共享内存和对共享内存的操作
    interface.regist_res("share_dict"                               , "res.share_dict")
    interface.regist_cmd("find", "impl.rg_cmd.rg_cmd_prj")

def list_res() :
    import  res
    for name,module in interface.registed_resource.items() :
        code = "obj = res.%s()" %(name)
        rg_logger.debug("exec code : %s" %code)
        try :
            exec code
            utls.rg_io.export_objdoc(name,obj )
        except  Exception as e :
            raise interface.rigger_exception("@list_res() code error: %s \n %s" %(code,e) )


#根据ioc容器实例化res对象
#用于help指令
def ins_res(name) :
    import  res
    for res_name,module in interface.registed_resource.items() :
        if  res_name == name :
            code = "obj = res.%s()" %(name)
            rg_logger.debug("exec code : %s" %code)
            try :
                exec code
                return obj
            except  Exception as e :
                raise interface.rigger_exception("@ins_res() code error: %s \n %s" %(code,e) )
    return None


def list_cmd() :
    import  impl.rg_cmd
    for name,module in interface.registed_cmd.items() :
        code = "obj = impl.rg_cmd.%s_cmd()" %(name)
        rg_logger.debug("exec code : %s" %code)
        try :
            exec code
            utls.rg_io.export_objdoc(name,obj )
        except  Exception as e :
            raise interface.rigger_exception("@list_cmd() code error: %s \n %s" %(code,e) )


#根据ioc容器实例化cmd对象
def ins_cmd(name) :
    import  impl.rg_cmd
    for cmd,module in interface.registed_cmd.items() :
        if  cmd == name :
            code = "obj = impl.rg_cmd.%s_cmd()" %(name)
            rg_logger.debug("exec code : %s" %code)
            try :
                exec code
                return obj
            except  Exception as e :
                raise interface.rigger_exception("@ins_cmd() code error: %s \n %s" %(code,e) )
    return None
