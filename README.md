# wechat-deleted-friends
查看被删的微信好友

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

