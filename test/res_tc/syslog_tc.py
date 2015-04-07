#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

class syslog_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_syslog_start(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_syslog.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"start -s syslog -e dev")

        expect = """
        python ${PRJ_ROOT}/src/utls/sysconf.py  -n RG_UT -f /etc/syslog.conf -t '#' -c 'None' -p file
        /usr/local/bin/syslog-ng reload
        """
        self.assertMacroEqual( expect, mock.cmds)
        # print(mock.cmds)

    def test_syslog_stop(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_syslog.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"stop -s syslog -e dev")

        expect = """
        python  ${PRJ_ROOT}/src/utls/sysconf.py  -n RG_UT -f /etc/syslog.conf -t '#' -c ''
        """
        self.assertMacroEqual( expect, mock.cmds)
        # print(mock.cmds)

