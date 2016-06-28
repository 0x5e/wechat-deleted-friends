# 查看被删的微信好友

## 注意

目前存在两个阻碍使用的问题，所以已经无法使用了，请后面来的同学们看看就好，不用尝试了。。。。谢谢大家的关注~

- 新建群组，添加好友的接口存在数量限制。在一定时间内添加的总人数超过一定数量后，接口就会无法使用。（幻想用随机数的童鞋放弃吧。。可能是你好友数量不够多？）
- 据V站朋友反馈(@kobe1941)：即使你已被对方删除好友，依然可以拉对方入群，所以该脚本工作的前提已不存在。

推荐两个相关项目：

[Urinx / WeixinBot](https://github.com/Urinx/WeixinBot)：网页版微信API，包含终端版微信及微信机器人

[geeeeeeeeek / electronic-wechat](https://github.com/geeeeeeeeek/electronic-wechat)：💬 A better WeChat on macOS and Linux. Fewer bugs, more features. Built with Electron by Zhongyi Tong.

协议相关文档：

[xiangzhai / qwx - 网页微信客户端封包大全](https://github.com/xiangzhai/qwx/blob/master/doc/protocol.md)

## 介绍

原理就是新建群组,如果加不进来就是被删好友了(不要在群组里讲话,别人是看不见的)

用的是微信网页版的接口

查询结果可能会引起一些心理上的不适,请小心使用..(逃

Mac OS用法:
启动Terminal

`$ python wdf.py`

按指示做即可

请确保requests模块已成功安装

`$ pip install requests   #安装requests模块`

### 暂未解决的问题

错误1205 "操作太频繁，请稍后再试。" (存在接口访问限制)

不清楚接口的限制策略是什么,有的同学能用有的不能用

打印被拉黑的列表(被限制了,没法测试..)

URLError (网络异常未处理)

最终会遗留下一个只有自己的群组,需要手工删一下

## 其他语言实现

[Go 版](https://github.com/miraclesu/wechat-deleted-friends)

[Node.js 版](https://github.com/chemdemo/wechat-helper)

[Chrome 插件](https://github.com/liaohuqiu/wechat-helper)

