#

#crontab 

管理 crontab 
``` yaml
  _sys:
      -  !R.system
          _name: "mysys"
          _res:
              - !R.echo
                  value : "hello"
              - !R.crontab
                  sudo: True
                  cron: "${PRJ_ROOT}/src/exampl.cron"
```

``` yaml
  _sys:
      -  !R.system
          _name: "mysys"
          _res:
              - !R.crontab
                  sudo: True
                  key : "A"
                  cron: "${PRJ_ROOT}/src/exampl1.cron"
               - !R.crontab
                  sudo: True
                  key : "B"
                  cron: "${PRJ_ROOT}/src/exampl2.cron"
```
