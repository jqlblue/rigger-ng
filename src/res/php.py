#coding=utf-8
import logging
import interface

from utls.rg_io  import rg_logger,rgio
from utls.rg_var import value_of
from utls.rg_sh  import shexec
from string import *

class php(interface.resource):
    """
    !R.PHP:
        bin: "/usr/local/bin/php"
        init: "init.sql"
    """
    bin       = "/usr/local/php-5.3/bin/php"

    def _allow(self,context) :
        return True
    def _before(self,context):
        self.bin = value_of(self.bin)

class python(interface.resource):

    """
    !R.PYRHON:
        bin: "python"
    """
    bin       = "python"

    def _allow(self,context) :
        return True

    def _before(self,context):
        self.bin = value_of(self.bin)
