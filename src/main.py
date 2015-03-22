#!/usr/bin/pylon.27
#coding=utf-8
import sys ,  os ,logging,getopt ,setting

#初始化运行环境
#将代码加入系统路径中
root  = os.path.dirname(os.path.realpath(__file__))
root  = os.path.dirname(root)
sys.path.append(os.path.join(root,"src") )


#设置日志的输出级别
#用户数据-d 是标示启动启动日志输出
#默认会数据error级别的日志
#当输入 1 时标示 打印info级别的日志
#输入 2 时表示输出debug级别的日志
#日志的输出会同步的console输出中

def setting_debug(opts) :
    log_level = logging.ERROR
    for opt,val in opts.items() :
        if opt == '-d' :
            setting.debug       = True
            setting.debug_level = int(val)
            if int(val) == 1 :
                log_level = logging.INFO
            if int(val) >= 2 :
                log_level = logging.DEBUG
    logging.basicConfig(level=log_level,filename='run.log')
    if setting.debug :
        console   = logging.StreamHandler()
        console.setLevel(log_level)
        # formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # console.setFormatter(formatter)
        logging.getLogger().addHandler(console)



#rg cmd(,cmd,...)  -s 系统或资源 -e 环境 -d 日志级别
#-c 加载配置文件的路径
if __name__ == '__main__':
    import interface,impl
    import impl.rg_run , impl.rg_args
    from   utls.rg_io import rgio

    #初始化IOC的容器
    impl.setup()
    #获得解析器同时解析用户的输入
    parser = impl.rg_args.rarg_parser()
    parser.parse(sys.argv[1:] )
    #设置日志的级别
    setting_debug(parser.argv)

    #以下代码没用到，可以删除？
    # opts,args = getopt.getopt(sys.argv[1:],"d:s:e:")
    #初始化默认参数的文件路径
    rars_file = os.getcwd() + "/_rg/.rigger-ng-v1.data"
    try :

        #rg cmd -s 系统或资源 -e 环境 -d 日志级别
        #-c 加载配置文件 默认 /_rg/conf.yaml 中
        #加载上一次的参数，返回参数实体
        #用于补全没输出参数的默认值
        #其中包含 -e 对环境变量 进行初始
        #-s 系统参数的初始化
        rargs  = impl.rg_args.run_args.load(rars_file)

        #跟新这次输入的指令作为默认值
        rargs.parse_update(parser)

        #rargs 是默认参数 parser。argv是输入参数
        impl.rg_run.run_rigger(rargs,parser.argv)

        #序列化 参数对象到相应文件
        #用于储存最上一次成功执行的参数 作为默认参数
        rargs.save(rars_file)

    except interface.user_break as e:
        rgio.error(e)
    except interface.badargs_exception  as e :
        print("\nerror:")
        rgio.error(e)
        runargs.help()
    except getopt.GetoptError as e:
        print("\nerror:")
        print(e)
        runargs.help()
    except interface.depend_exception as e :
        e.monitor.out()
    # except interface.rigger_exception as e:
    #      rgio.error(e)
