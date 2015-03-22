#!/bin/bash
current_date=`date ""+%Y%m%d` #当前的日期（ 年月日 ）

todaylog="../data/daemon_test.txt" #今天的日志文件名

echo "start"

#如果日志文件不存在，创建一个
if [ ! -f $todaylog ]

then

    touch $todaylog

fi

#输出日志到日志文件
log_time_format=`date "+%Y-%m-%d %T"`

echo "${log_time_format} commands start.....">>${todaylog}

# commands blocks

sleep 4

log_time_format=`date "+%Y-%m-%d %T"`

echo "${log_time_format} commands end!">>${todaylog} #结束时记录日志
