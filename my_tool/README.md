# Summary Local API Tool
本地简易Flask接口，SQLite存储对话摘要，带Token鉴权

## 环境依赖
```bash
pip install -r requirements.txt
```
## 启动服务
```bash
python api_server.py
```
服务地址：http://127.0.0.1:5099

## 鉴权方式
所有接口请求头必须携带Token：
`Authorization: Bearer local_dev_token`

## 接口列表
1. POST /summaries
新增摘要记录，请求体需传入 user_id、summary_text，可选 tags 数组

2. GET /summaries?user_id=xxx
查询指定用户全部摘要，可追加参数 keyword 做关键词模糊搜索

3. DELETE /summaries/{id}
根据数据 id 删除单条摘要

## 常见问题
1. 浏览器访问 127.0.0.1:5099 提示无法访问
解决：打开终端执行 `python api_server.py` 启动服务，终端窗口不能关闭

2. 调用接口返回 401
解决：请求头缺少正确的 Bearer Token

3. 依赖包缺失报错
解决：在项目目录执行 `pip install -r requirements.txt`

## 简要说明
1，主要作用
总结用户与本地部署ai的对话并保存到数据库里面，后续部署的ai调用数据库内容，让ai了解用户主要目标

2，更改问题
这个程序我自己写了一个框架让ai帮我补全的，如果要实现类似于让另一个平台的ai模型继续对话也是可以实现的，让ai改一下关于数据库数据录入相关就行，还有就是需要联网调用数据库的话也是可以实现的，将数据库部署到云端重写连接代码。

3，使用问题
我自己是本地部署了千问和deepseek的两个小模型来试用的，别的应该没有什么大问题
