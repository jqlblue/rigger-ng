#内建机制

## env
``` yaml
  _env:
      - !R.env
          _name    : "dev"
          prj_root : "${HOME}/devspace/rigger-ng/demo"
      - !R.env
          _name    : "centos"
          prj_root : "${HOME}/devspace/rigger-ng/demo"
```

## system

``` yaml
  _sys:
      -  !R.system
          _name : "test"
          _res  :
              - !R.vars
                      TEST_CASE : "${PRJ_ROOT}/test/main.py"
              - !R.echo
                  value         : "${TEST_CASE}"
```

## modul & using


通过 modul 和 using 为rg 提供了复用机制

### 示例
``` yaml
_mod:
    - !R.modul
        _name : "m1"
        _res  :
            - !R.vars
                test_case : "A"
            - !R.echo
                value : "${TEST_CASE}"
            - !R.assert_eq
                value : "${TEST_CASE}"
                expect : "A"
```
``` yaml
- !R.using
    path          : "${PRJ_ROOT}/_rg/modul.yaml"
    modul         : "m1"
```

# 内建资源
## echo
```
      - !R.echo
          value         : "${PRJ_ROOT}"
```
## assert_eq

```
      - !R.assert_eq
          value  : "${Y}"
          expect : "hello"
```
# 扩展资源

## daemon
示例:
``` yaml

```
属性:
```
property:
	 forever         : "True"
	 script          : ""
	 logpath         : "${RUN_PATH}"
	 confpath        : "${PRJ_ROOT}/conf/used"
	 umask           : "022"
	 tag             : ""
	 daemon          : "True"
	 zdaemon         : "/usr/local/python/bin/zdaemon"
	 runpath         : "${RUN_PATH}"
```
#帮助

*通过 rg help res 可以查看资源列表*
*通过 rg help res <youres> 可以查看 youres 资源的具体信息*
