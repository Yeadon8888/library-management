# 图书管理系统

一个基于Flask的图书馆管理系统，提供图书管理、借阅、评论等功能。

![image-20241110112014033](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112014033.png)

## 功能特点：
- 用户认证（登录/注册）
- 图书管理（增删改查）
- 图书借阅和归还
- 图书评论和评分
- 图书预约
- 管理员后台管理

## 系统要求：
- Python 3.7+
- SQLite 3

## 安装步骤：

1. 安装 Python 依赖：
   ```bash
   pip install -r requirements.txt

2. 初始化数据库：

   ```bash
   python init_db.py
   ```
3. 运行应用：

   ```bash
   python run.py
   ```

## 项目结构：

```
library_system/
├── run.py                 # 应用入口文件
├── config.py              # 配置文件
├── init_db.py            # 数据库初始化脚本
├── requirements.txt      # 项目依赖
└── app/
    ├── __init__.py      # 应用初始化
    ├── models/          # 数据模型
    │   ├── book.py     # 图书模型
    │   ├── user.py     # 用户模型
    │   ├── loan.py     # 借阅模型
    │   ├── comment.py  # 评论模型
    │   └── reservation.py # 预约模型
    ├── routes/         # 路由控制器
    │   ├── auth.py    # 认证相关路由
    │   ├── book.py    # 图书相关路由
    │   ├── loan.py    # 借阅相关路由
    │   └── main.py    # 主页路由
    ├── static/        # 静态文件
    │   ├── css/      # CSS样式
    │   └── js/       # JavaScript脚本
    └── templates/     # 模板文件
        ├── auth/     # 认证相关模板
        ├── book/     # 图书相关模板
        ├── loan/     # 借阅相关模板
        └── base.html # 基础模板
```

## 主要功能模块：

### 用户管理 (app/routes/auth.py)

- 用户注册 /register
  - 用户名和邮箱唯一性验证
  
  - 密码强度验证
  
    ![image-20241110112104257](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112104257.png)
  
- 用户登录 /login

  ![image-20241110112047071](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112047071.png)

- 用户登出 /logout

- 个人信息管理 /profile

### 图书管理 (app/routes/book.py)

- 图书列表 /books
- ![image-20241110112537721](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112537721.png)
- 图书详情 /book/`<id>`
- ![image-20241110112802014](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112802014.png)
- 添加图书 /book/add (管理员)
- 编辑图书 /book/`<id>`/edit (管理员)
  - 修改基本信息（ISBN、书名、作者等）
  - 调整库存数量（自动计算可用库存）
  - 修改图书分类
  - ![image-20241110112238459](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112238459.png)
- 删除图书 /book/`<id>`/delete (管理员)
  - 删除前检查是否有未归还的借阅
  - 确认对话框防止误操作
  - ![image-20241110112250402](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112250402.png)
- 图书搜索 /books/search
  - 支持按书名、作者、ISBN搜索
  - 支持按类别筛选
  - ![image-20241110153047382](C:/Users/86151/AppData/Roaming/Typora/typora-user-images/image-20241110153047382.png)
- 图书评论 /book/<book_id>/comment
  - 评分系统（1-5星）
  - 评论审核功能
  - ![image-20241110112517854](https://yeadon-picture.oss-cn-qingdao.aliyuncs.com/img/image-20241110112517854.png)

### 借阅管理 (app/routes/loan.py)

- 借书 /book/<book_id>/borrow
  - 库存检查
  - 借阅数量限制
- 还书 /book/<book_id>/return
- 借阅记录 /my-loans
  - 显示当前借阅
  - 逾期提醒

## 数据模型：

### User (app/models/user.py)

- id: 用户ID
- username: 用户名
- email: 邮箱
- password_hash: 加密密码
- is_admin: 管理员标志

### Book (app/models/book.py)

- id: 图书ID
- isbn: ISBN号
- title: 书名
- author: 作者
- publisher: 出版社
- category: 类别
- total_copies: 总库存
- available_copies: 可用库存

### Loan (app/models/loan.py)

- id: 借阅ID
- user_id: 用户ID
- book_id: 图书ID
- borrow_date: 借阅日期
- due_date: 应还日期
- return_date: 实际归还日期
- status: 借阅状态

### Comment (app/models/comment.py)

- id: 评论ID
- user_id: 用户ID
- book_id: 图书ID
- content: 评论内容
- rating: 评分
- created_at: 创建时间
- is_approved: 审核状态

## 配置说明：

在 config.py 中配置：

- SQLALCHEMY_DATABASE_URI: 数据库连接
- SECRET_KEY: 安全密钥
- MAIL_SERVER: 邮件服务器（可选）
- MAIL_PORT: 邮件端口
- MAIL_USERNAME: 邮箱用户名
- MAIL_PASSWORD: 邮箱密码

## 默认管理员账户：

- 用户名：admin
- 密码：admin123
- 邮箱：admin@example.com

## 安全注意事项：

1. 生产环境部署前必须修改：

   - 默认管理员密码
   - SECRET_KEY
   - 数据库配置
2. 密码安全要求：

   - 最少8位
   - 必须包含大小写字母
   - 必须包含数字
3. 借阅限制：

   - 每人最多同时借阅5本书
   - 标准借期为30天
   - 超期将进行提醒

## 开发指南：

1. 代码规范：

   - 遵循 PEP 8 规范
   - 使用清晰的命名约定
   - 添加适当的注释
2. 数据库操作：

   - 使用 SQLAlchemy ORM
   - 正确处理事务
   - 注意并发安全
3. 前端开发：

   - 模板继承自 base.html
   - 使用 Bootstrap 5 框架
   - JavaScript 代码模块化
4. 测试建议：

   - 编写单元测试
   - 进行功能测试
   - 测试边界情况

## License：

MIT License
Copyright (c) 2024

```

```
