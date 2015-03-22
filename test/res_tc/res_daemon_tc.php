<?php


#在daemon中启动一个worker，
##遇到异常情况时daemon会重启worker
#执行stop时daemon进程会消耗从而停止所有只经常
class Worker
{

    public function run()
    {
        try{
            $file = fopen('../data/daemon_test.txt', 'a+'); // a模式就是一种追加模式，如果是w模式则会删除之前的内容再添加
        }catch(Exception $e)
        {
            print $e;
        }

        // 获取需要写入的内容
        $c = 'i am php write';
        // 写入追加的内容
        fwrite($file,$c);
        $i = 1;
        while(true)
        {
            if($i==10)
            {
                // 关闭b.php文件
                fclose($file);
                // 销毁文件资源句柄变量
                unset($file);
                break;
                // throw new RuntimeException();
            }
            fwrite($file,$i);
            $i++;

        }

        sleep(4);
    }
}

$worker = new Worker();
$worker->run();

