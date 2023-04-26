# SpiderController

您现在查看的是一个基于Django框架和scrapy的可视化爬虫程序，我们的目标是使爬虫程序摆脱代码的束缚，以可视化的形式对站点内容进行爬取，计划于 2023-07 之前完成基本功能的开发，感谢您的关注。

## 🤖 Usage

请在您的主机上安装 Anaconda 程序以便管理 python 环境。

```powershell
conda create SpiderController
conda activate

# 安装依赖
pip install -r requirements.txt

# 创建数据库表
python manage.py migrate

# 创建管理员账户
python manage.py createsuperuser

# 运行 django
python manage.py runserver 8080


# 你会在浏览器中看到程序页面，如果没有出现，请访问 http://127.0.0.1:8080
```