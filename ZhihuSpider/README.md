# Scrapy
## 爬取知乎
知乎登陆严重模式
- client_id: c3cef7c66a1843f8b3a9e6a1e3160e20
- grant_type: password
- timestamp: 当前时间戳
- source: com.zhihu.web
- username: 用户名（手机号邮箱）
- password: 密码
- signature：根据上面这些数据加上一个 secret 动态生成 

由于secret无法找到，所以web端登陆模拟不了，无法对问题进行深度优先爬取，只能针对特定的问题进行问题答案爬取。这里推荐一个库[Zhihu-OAuth](https://github.com/7sDream/zhihu-oauth)该库破解了安卓端的模拟登陆，可满足爬虫需求。

针对问题29814297的爬取结果
![爬娶结果](http://ows764enq.bkt.clouddn.com/zhihu29814297.png)