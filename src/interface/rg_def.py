#coding=utf-8
import logging,copy
import rg_conf
import utls.rg_sh ,utls.rg_io
from utls.rg_io import rg_logger

#运行时的上下文对象
#可以讲运行时的信息传入这个对象中
#在整个调用栈中贯穿
class run_context :
    def __init__(self):
        self.restore = None
    def keep(self) :
        self.restore =  copy.copy(self.__dict__)
    def rollback(self):
        self.__dict__=  copy.copy(self.restore)
        self.restore = None

#指令集的抽象类
#应该先添加指令是可以再此类中添加
#同时默认的指令已下划线开头_cmd
#添加的指令直接cmd 如find
class controlable :
    sudo = False
    def _allow(self,context):
        pass
    def _before(self,context):
        pass
    def _after(self,context):
        pass
    def _start(self,context):
        pass
    def _stop(self,context):
        pass
    def _reload(self,context):
        pass
    def _config(self,context):
        pass
    def _data(self,context):
        pass
    def _check(self,context):
        pass
    def _clean(self,context):
        pass
    def _info(self,context):
        return ""

   #新添加的指令
    def find(self,context):
        pass

    def shell(self,context):
        pass

    def depend(self,context):
        pass

#以aop的方式执行以减少代码量和增加可扩展性
def control_call(res,fun,context,tag) :
    #主要控制日志的输入
    #设置日志的缓存buf和 输出的资源及tag
    with utls.rg_io.scope_iotag(res.__class__.__name__ ,tag) :
        if res._allow(context) :
            #设置shell执行的开关
            with utls.rg_sh.scope_sudo(res.sudo) :

                    #放入运行栈
                    utls.rg_io.run_struct.push( res.__class__.__name__)

                    res._before(context)
                    fun(res,context)
                    res._after(context)

                    #出运行栈
                    utls.rg_io.run_struct.pop()


#指令集的容器和递归调用的中间件
#添加指令时需要实现controlable 接口的方法
class control_box(controlable):

    #在初始化资源对象时会将配置文件默认conf.yaml中的
    #_res实例化到响应的对象（env，project，system ）中
    #同时在new 递归入口prj_main 是将 资源的头结点
    #apped到_res中
    def __init__(self):
        self._res = []

    #循环执行注册（append）进去的资源
    def items_call(self,fun,context,tag):
        for r in self._res :
            control_call(r,fun,context,tag)

    def _start(self,context):
        fun = lambda x,y : x._start(y)
        self.items_call(fun,context,'_start')

    def _stop(self,context):
        fun = lambda x,y : x._stop(y)
        self.items_call(fun,context,'_stop')

    def _config(self,context):
        fun = lambda x,y : x._config(y)
        self.items_call(fun,context,'_config')

    def _data(self,context):
        fun = lambda x,y : x._data(y)
        self.items_call(fun,context,'_data')

    def _check(self,context):
        fun = lambda x,y : x._check(y)
        self.items_call(fun,context,'_check')

    def _reload(self,context):
        fun = lambda x,y : x._reload(y)
        self.items_call(fun,context,'_reload')

    def _clean(self,context):
        fun = lambda x,y : x._clean(y)
        self.items_call(fun,context,'_clean')

    def _info(self,context):
        fun = lambda x,y : x._info(y)
        self.items_call(fun,context,'_info')

    #自定义方法，用于share_dict
    def find(self,context):
        fun = lambda x,y : x.find(y)
        self.items_call(fun,context,'find')

    def shell(self,context):
        fun = lambda x,y : x.shell(y)
        self.items_call(fun,context,'shell')

    def depend(self,context):
        fun = lambda x,y : x.depend(y)
        self.items_call(fun,context,'depend')

    def _allow(self,context):
        return True
    def append(self,item):
        self._res.append(item)
    def push(self,item):
        self._res.insert(0,item)


    def _check_print(self,is_true,msg):
        print(msg)

    def _resname(self):
        tag = self.__class__.__name__
        return tag

class resource (controlable,rg_conf.base):
    allow_res   = "ALL"
    def _allow(self,context):
        allowd =  self.allow_res == "ALL"  or self.allow_res == self.clsname()
        if allowd:
            rg_logger.debug( "allowd resource %s ,current resouce is %s " %(self.allow_res,self._resname()))
        return  allowd

    def _check_print(self,is_true,msg):
        if is_true:
            print( "\t%-100.100s%-20.20s-[Y]" % (msg ,self._resname())  )
        else:
            print( "\t%-100.100s%-20.20s-[ ]" % (msg ,self._resname())  )
    def _resname(self):
        tag = self.__class__.__name__
        return tag
