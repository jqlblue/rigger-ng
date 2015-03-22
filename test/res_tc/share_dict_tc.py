#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

from utls.rg_sh  import shexec

class sdict_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_sdict(self) :

        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_share_dict.yaml")
        #     self.asst_cmd(conf,"data -s sdict ")
        # cmdtpl  = ''
        # shexec.execmd(Template(cmdtpl).substitute(MYSQL=mysql,HOST=self.host ,DBNAME=self.name,USER=self.user,PASSWD=self.password,SQL=self.init),True)
        # print(mock.cmds)

