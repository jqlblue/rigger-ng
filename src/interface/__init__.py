# -*- coding: utf-8 -*-

from  rg_conf import base
from  rg_def  import resource , run_context , controlable , control_box ,control_call
from  rg_err  import *
#存放资源容器，这些资源包含mysql，和email等服务
registed_resource = {}

#存放指令集的容器 包含info
registed_cmd      = {}

#注册资源
def regist_res(name,module) :
    name = name.split(',')
    for  res in name:
        registed_resource[res] = module

#注册指令
def regist_cmd(name,module) :
    name = name.split(',')
    for  c in name:
        registed_cmd[c] = module
