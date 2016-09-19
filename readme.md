windows单机单进程版vn.py交易模块

具体的接口若干，其中okcoins是比特币，不想用它可以在vtEngine.py中注释掉(本例子中已注释)，ib为外盘的盈透证券，也已注释。

使用方法：

1.安装anaconda32位版(因为CTP在windows下常用的接口是32位的，想用64位需要重新编译)
2.安装微软vc redist 2013 (x86)
3.执行start_trading_win.bat脚本

调试并编写代码方法：

在满足以上运行条件后，

1.安装pycharm社区版

2.使用pycharm将本文件夹打开

3.首次调试：

点击上面的工具栏run->debug...

然后选择script为vtMain.py，开始调试

4.以后每次调试策略可以直接按debug的快捷键(可以在pycharm的file->settings里面设置快捷键)

编写新策略
1.策略例子在本项目的ctaAlgo/ctaDemo.py里面，添加新策略可以模仿现有的双EMA均线策略编写，写好策略后在配置文件CTA_setting.json中添加此新策略的信息

2.ctp的接口和账户配置在ctpGateway/CTP_connect.json里面，填入你自己的brokerID和账号密码以及经纪商提供的IP和端口

3.开始交易/调试:
进入界面后点击：系统->连接CTP，登录CTP账号
然后加载并开始策略：算法->CTA策略