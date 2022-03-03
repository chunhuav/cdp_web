# 确保 Unomi 已经运行
```shell
./bin/karaf
```
输出
```shell
karaf: JAVA_HOME not set; results may vary
        __ __                  ____
       / //_/____ __________ _/ __/
      / ,<  / __ `/ ___/ __ `/ /_
     / /| |/ /_/ / /  / /_/ / __/
    /_/ |_|\__,_/_/   \__,_/_/

  Apache Karaf (4.2.8)

Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown Karaf.

karaf@root()> Initializing Unomi...


        ____ ___     A P A C H E     .__
       |    |   \____   ____   _____ |__|
       |    |   /    \ /  _ \ /     \|  |
       |    |  /   |  (  <_> )  Y Y  \  |
       |______/|___|  /\____/|__|_|  /__|
                    \/             \/

--------------------------------------------------------------------------
  1.5.7  Build:7abee  Timestamp:1627053381505
--------------------------------------------------------------------------
Successfully started 27 bundles and 2 required services in 36548 ms
```
# Install Py4web
https://py4web.com/_documentation/static/en/chapter-03.html

#更改文件
修改 controolers.py 中 line 43

unomi_url = "http://3.113.215.104:8181/"



# 启动py4web
```shell
py4web run apps
```
输出
```
Ombott v0.0.12 server starting up (using RocketServer(reloader=False))...
watching (lazy-mode) python file changes in: /Users/liuchunh/01AWS/02_Industry_solution_project/CDP/cdp_ui/apps
Listening on http://127.0.0.1:8000/
Hit Ctrl-C to quit.
```

#使用 CDP
在浏览器中输入
http://127.0.0.1:8000/cdp
开始使用 CDP
