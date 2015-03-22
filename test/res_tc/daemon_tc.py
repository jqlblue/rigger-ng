#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

class daemon_tc(base.tc_tools.rigger_tc):

    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_start_daemon(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_daemon.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"start -s daemon -e dev")

        expect = """
        python  /usr/local/bin/zdaemon  -C /home/chenrishen/devspace/rigger-ng/run//zdaemon-1-3c8f296dc71f64443020f3a0ab6106ba.xml  start
        """
        self.assertMacroEqual( expect, mock.cmds)
        # print(mock.cmds)

    def test_stop_daemon(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_daemon.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"stop -s daemon -e dev")

        expect = """
        python  /usr/local/bin/zdaemon  -C /home/chenrishen/devspace/rigger-ng/run//zdaemon-1-3c8f296dc71f64443020f3a0ab6106ba.xml  stop
        """
        self.assertMacroEqual( expect, mock.cmds)
