#coding=utf-8
import interface
import base.tc_tools
import os

from impl.rg_yaml  import *
import utls.rg_var
class yaml_conf_tc(base.tc_tools.rigger_tc):
    def test_resyaml(self):

        root   = utls.rg_var.value_of("${HOME}/devspace/rigger-ng")
        loader = conf_loader( root + "/test/impl_tc/prj_struct.yaml")
        data   = loader.load_data("!R","res")
        rars_file = os.getcwd() + "/_rg/.rigger-ng-v1.data"
        print "==================="
        print rars_file
        # print(data['__prj'].name)
        # print(data['__sys'][0].name)
