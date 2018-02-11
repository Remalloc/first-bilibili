# first-bilibili v1.0
##  python B站抢楼程序
  该程序可以快速抢到B站某个UP主的一楼 :)


***
## 快速开始
* 登录B站
- 获取Cookie值 以chrome浏览器为例：
  ![cookie](https://github.com/Remalloc/first-bilibili/blob/master/img/cookie.png)
* 记录如下Cookie值：
  * **DedeUserID**
  * **DedeUserID__ckMd5**
  * **SESSDATA**
  * **bili_jct**
- 替换 **post_comment** 函数中的Cookie
  ```python
  def post_comment(aid, message):
    reply_url = "https://api.bilibili.com/x/v2/reply/add"
    cookie = {
        "DedeUserID": "",  # 用户ID
        "DedeUserID__ckMd5": "",  # 用户ID_MD5值
        "SESSDATA": "",  # 会话cookie
        "bili_jct": ""  # crsf cookie
    }
  ```
* 进入UP主的空间,找到ID
  [https://space.bilibili.com/221648](https://space.bilibili.com/221648)
  ID:221648
  
  ```python
  if __name__ == '__main__':
    mid = 221648  # UP主ID号
    message = "第一"  # 留言内容
   ```
  
- 运行程序
  * 程序会每1秒检测一次UP主是否更新视频
  * 如果想要更改检测频率可以更改main中的time.sleep的值
