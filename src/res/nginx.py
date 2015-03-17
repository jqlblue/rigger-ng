#coding=utf-8
import logging
import interface

from utls.rg_io  import rg_logger
import files

class nginx (interface.resource):
    """support nginx"""
    _need_reload = True
    _sudo        = True
    def local(self,context):
        self.sudo       = env_exp.value(self.sudo)
        self.need_reload = env_exp.value(self.need_reload)

    def start(self,context):
        self.reload(context)
    def stop(self,context):
        pass
    def reload(self,context):
        if self.need_reload  :
            cmd = get_env_conf().nginx_ctrl + ' reload '
            rg_sh.shexec.execmd(cmd)
    def check(self,context):
        # cmd = "ps auxww | grep nginx   "
        # check_proc("Nginx",cmd)
        ngx_test = get_env_conf().nginx_ctrl.replace(" -s","")
        ngx_test += " -t "
        cmd = " sudo rm -rf /tmp/nginx_ok  ; if  " +  ngx_test + "  ; then  sudo  touch  /tmp/nginx_ok ;  fi  "
        rg_sh.shexec.execmd(cmd)
        self.check_print(os.path.exists("/tmp/nginx_ok"),"nginx conf")

class nginx_conf_tpl(files.file_tpl):
    _mod    = "a+w"
    def config(self,context):
        files.file_tpl.config(self,context)
        dst_path  = get_env_conf().nginx_conf_path 
        tpl =  'if test  -L $PATH/$DST ; then rm $PATH/$DST ; fi; ln -s $SRC $PATH/$DST'
        cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
        rg_sh.shexec.execmd(cmd)
    def clean(self,context):
        dst_path  = get_env_conf().nginx_conf_path 
        tpl =  'if test -L $PATH/$DST ; then rm $PATH/$DST ; fi ; if test -e $SRC ; then  rm  $SRC; fi ;'
        cmd = Template(tpl).substitute(PATH=dst_path, DST=os.path.basename(self.dst), SRC=self.dst)
        rg_sh.shexec.execmd(cmd)
