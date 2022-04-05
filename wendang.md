## 暂时文档

1. 静态页面结构

   admin/	自带后台

   lf/	失物招领

   report/ 	权益投诉

   tips/		柜君tips

   qa/ 	Q&A

   user/ 	个人中心

   login/	登入界面

   api/ 接口

   直接访问网址，直接redirect（重定向）到/lf页面上

2. 接口设计

   GET和POST的规范，类似于清华大学类似项目的文档。**各种API接口返回JSON格式！！！**

   ### 一、失物招领相关接口

   - api/lf/list	列表。使用GET方法。接口如下：

     | 参数     | 类型             | 作用               |
     | -------- | ---------------- | ------------------ |
     | title    | 字符串           | 搜索标题中的字符   |
     | date_old | YYYY-MM-DD       | 最近日期           |
     | date_new | YYYY-MM-DD       | 最远日期           |
     | place    | 字符串           | 丢失地点           |
     | name     | 字符串           | 丢失物品           |
     | page     | 数字             | 第几页(一页N=20条) |
     | type     | 单个字符'L'或'F' | 类型（默认为'F'）  |

     返回格式。界面类似于百度贴吧。

     ```json
     {
         "result" : "success",
         "total_page" : 5,
         "privilege" : "root",
         "data" : [
             {
             	"title" : "丢了一把伞，求助!",
                 "date_old" : "2022-03-05",
                 "date_new" : "2022-03-05",
                 "place" : "一教",
                 "name" : "伞",
                 "type" : 'L',
                 "release_time" : "2022-03-06",
                 "author" : "annoymous123456",
                 "status" : 1,
         		"public" : true
         	},......
         ]
     }
     ```

     所有项均不必须。

     status = 0 表示"还没找到"，=1表示"已经被捡到了等待确认",=2表示"已经找到"(虽然按照现在的设计，已经找到会被删除，但目前还是这样)。

     total_page表示这个搜索一共有多少页，从而让前端决定是否使用分页。

     date_old和date_new返回丢失时间的范围。

     privilege表示特权，有三档：root，admin，guest。

     public表示是否公开。

     其他内容可以根据对应的英文名称猜测其意思，不再赘述。

   - api/lf/release 发布。使用POST方法。接口如下：

     | 参数  | 类型             | 作用             |
     | ----- | ---------------- | ---------------- |
     | title | 字符串           | 搜索标题中的字符 |
     | date  | YYYY-MM-DD       | 日期             |
     | place | 字符串           | 丢失地点         |
     | name  | 字符串           | 丢失物品         |
     | text  | 字符串           | 文字内容         |
     | pic1  | 二进制流         | 图片1            |
     | pic2  | 二进制流         | 图片2            |
     | pic3  | 二进制流         | 图片3            |
     | type  | 单个字符'L'或'F' | 类型             |
     | public | 布尔型          | 是否公开         |

     除了文字和图片以外，所有项均必须。可以考虑增加图片的最大上传数量，参数类似。返回结果：

     ```json
     {
         "result" : "success",
         "id" : 123456
     }
     ```

     并重定向到该帖子上去。（若失败则为fail，并附上msg表示错误信息）

   - api/lf/delete 删除帖子。使用POST方法。接口如下：

     | 参数 | 类型 | 作用   |
     | ---- | ---- | ------ |
     | id   | 数字 | 帖子id |

     返回结果：

     ```json
     {	"result": "sucess"	}
     ```

   - api/lf/pick 捡到失物。所有项目与上一条同。

   - api/lf/reply 回复帖子。使用POST方法。接口如下：

     | 参数 | 类型     | 作用     |
     | ---- | -------- | -------- |
     | post_id   | 数字     | 帖子id   |
     | text | 字符串   | 文字内容 |
     | pic1 | 二进制流 | 图片1    |
     | pic2 | 二进制流 | 图片2    |
     | pic3 | 二进制流 | 图片3    |
     | public | 布尔型 | 是否公开   |

     返回结果同上，即只有一个result。

   - api/lf/?????? 询问某个帖子的数据，还没想好应该是什么。

   - lf/ 查看主页。GET方法，无参数，返回HTML页面。

   - lf/[%d] 查看id=%d某一条帖子。GET方法，无参数，返回查看帖子的HTML页面。


   ### 二、用户相关的接口

   - api/auth/captcha	发送验证码。POST方法：参数如下

     | 参数  | 类型   | 作用     |
     | ----- | ------ | -------- |
     | email | 字符串 | 科大邮箱 |

     返回格式：result。。。。（同上）

   - api/auth/register 注册。POST方法。参数如下：

     | 参数     | 类型   | 作用     |
     | -------- | ------ | -------- |
     | email    | 字符串 | 科大邮箱 |
     | username | 字符串 | 用户名   |
     | password | 字符串 | 密码     |
     | captcha  | 字符串 | 验证码   |

     返回格式：同上。后端将会设置username长度为[1，20]，密码长度为[6，20]，否则返回错误。

   - api/auth/login 登陆。POST方法，参数如下：

     | 参数     | 类型   | 作用             |
     | -------- | ------ | ---------------- |
     | username | 字符串 | 用户名或科大邮箱 |
     | password | 字符串 | 密码             |

     返回格式：同上。

   - api/auth/forget 忘记密码。 POST方法，参数如下：

     | 参数     | 类型   | 作用     |
     | -------- | ------ | -------- |
     | email    | 字符串 | 科大邮箱 |
     | password | 字符串 | 密码     |
     | captcha  | 字符串 | 验证码   |

     调用此方法前必须先调用captcha获得验证码。返回同上。

   - api/auth/logout 登出。POST方法，无参数，返回同上。前端可能需要redirect一下子。

   - api/auth/chpwd 更换密码。POST方法。必须登录后访问。参数是：

     | 参数 | 类型   | 作用   |
     | ---- | ------ | ------ |
     | old  | 字符串 | 原密码 |
     | new  | 字符串 | 后密码 |

     返回同上。

   - api/auth/update 更换信息。POST方法。必须登录后访问，参数是：

     | 参数                     | 类型         | 作用   |
     | ------------------------ | ------------ | ------ |
     | username                 | 字符串       | 用户名 |
     | mobile                   | 纯数字字符串 | 手机号 |
     | qq                       | 纯数字字符串 | qq号   |
     | name                     | 字符串       | 姓名   |
     | stu_id                   | 纯数字字符串 | 学号   |
     | 不准更改邮箱。返回同上。 |              |        |

   - api/auth/user/<%d> 用户信息。GET方法，参数是用户的uid。必须是登陆状态。返回信息：

     ```
     {
     	email: "...@...",
     	username: "",
     	mobile : "",
     	qq : "",
     	name : "",
     	stu_id : ""
     }
     ```

     类似等等。

   - api/auth/me 自己的信息。GET方法，等同于api/auth/user/{self.id}

   - 为什么没有提升管理员权限的api

     因为django有个后台，可以管理用户权限，我直接在后台设置super user就可以了。

     

   3.数据库格式

   ### 一、帖子在数据库里的格式

   | 字段   | 类型         | 说明      |
   | ------ | ------------ | --------- |
   | id     | Auto         | 自增id    |
   | author | Char[32]     | 作者      |
   | date   | Date         | 最早      |
   | place  | Char[64]     | 地点      |
   | name   | Char[64]     | 物品      |
   | title  | char[64]    | 标题    |
   | text   | Char[256]    | 描述      |
   | pic1   | FilePath    | 图片1地址 |
   | pic2   | FilePath    | 图片2地址 |
   | pic3   | FilePath    | 图片3地址 |
   | public | Bool         | 是否公开  |
   | time   | DateTime     | 发帖时间  |
   | status | SmallInteger | 状态值    |
   | type   | Char[1]      | 类型      |

   (未完待续，第一版中，没有验权机制。)

:::warning
为了压缩空间，或许可以考虑把status和type放在一起（
:::

数据库格式之后不更了，看代码就行（雾）
