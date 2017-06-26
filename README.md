# huangAdmin

### Introduction

This project is used for Flask to build admin management. The difference between Flask-Admin and huangAdmin is that huangAdmin is built based on SPA(Single Page Application). Because of this, We can have a much better experience with huangAdmin than Flask-Admin.

Another reason for me to build huangAdmin is my code is more clear than other project. So if somebody want to learn how to build your own Flask Admin, a good idea is to start from my code.

### Installation

```bash
pip install -e git+https://github.com/huang502/huangAdmin.git@master#egg=huangAdmin
```

### Example

```python
# app 是你的Flask app实例, db 是你的db实例， [User, Article]是你想管理的model
from huangadmin import huangAdmin
ca = huangAdmin(app, db, [User, Article])
ca.init_app()
```

完整实例代码在test文件夹中，这边提供了一个运行脚本run.sh，直接执行脚本即可运行实例代码。
运行成功之后访问127.0.0.1:5000/admin/ 即可。

截图:
![create](https://raw.githubusercontent.com/huang502/huangAdmin/master/examples/create.gif)
![delete](https://raw.githubusercontent.com/huang502/huangAdmin/master/examples/delete.gif)
![list](https://raw.githubusercontent.com/huang502/huangAdmin/master/examples/list.gif)
![edit](https://raw.githubusercontent.com/huang502/huangAdmin/master/examples/edit.gif)

### Bug

保存和编辑之后不会立即生效，需要刷新页面。
