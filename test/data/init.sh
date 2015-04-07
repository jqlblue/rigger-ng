#!/bin/bash
echo $PRJ_ROOT
case $1 in
        start)
           echo " ${PRJ_ROOT}  start";;
        stop)
           echo "stop";;
        data)
           echo "data";;
        config)
           echo "config";;
        clean)
           echo "clean";;
        reload)
           echo "reload";;
        check)
           echo "check";;
        shell)
           echo "shell";;
esac




