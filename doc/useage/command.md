

# 系统控制
## conf

```
rg conf -e <env> -s <sys>
```
## start,stop,restart,reload

```
rg start [-s <sys>]
rg stop  [-s <sys>]
rg restart [-s <sys>]
rg reload [-s <sys>]
```

# 其它
## init
```
rg init 
```

## tpl 


```
rg tpl -t <tpl path> -o <dest path>
```

可以通过tpl指令, 生成新工程
