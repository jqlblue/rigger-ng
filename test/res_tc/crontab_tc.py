#coding=utf8
import  logging
import  utls.tpl ,interface ,base.tc_tools
import  impl.rg_args

class crontab_tc(base.tc_tools.rigger_tc):
    def asst_cmd(self,conf,cmd):
        impl.rg_run.run_cmd(cmd,conf)

    def test_crontab_start(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_crontab.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"start -s crontab -e dev")

        expect = """
        crontab -l >  /tmp/${USER}_RG_UT_crontab.cron ;
        python ${PRJ_ROOT}/src/utls/sysconf.py  -n RG_UT_crontab -f /tmp/${USER}_RG_UT_crontab.cron -t '#' -c ${PRJ_ROOT}/test/data/crontab.cron -p file ;
        crontab /tmp/${USER}_RG_UT_crontab.cron
        """
        self.assertMacroEqual( expect, mock.cmds)
        # print(mock.cmds)

    def test_crontab_stop(self) :
        conf = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/res_tc/res_crontab.yaml")
        mock = base.tc_tools.res_mock()
        with   mock :
            self.asst_cmd(conf,"stop -s crontab -e dev")

        expect = """
        crontab -l >  /tmp/${USER}_RG_UT_crontab.cron ;
        python ${PRJ_ROOT}/src/utls/sysconf.py  -n RG_UT_crontab -f /tmp/${USER}_RG_UT_crontab.cron -t '#' -c ''  ;
        crontab /tmp/${USER}_RG_UT_crontab.cron
        """
        self.assertMacroEqual( expect, mock.cmds)



