# 开发过程记录

这里使用了conda作为包管理工具，拉取项目之后，创建python==3.10的conda环境

在conda环境中运行 pip install -r requirements.txt 来安装依赖

## Django

### 创建一个django框架

```bash
django-admin startproject mysite
```

运行django

```bash
python manage.py runserver
```

你会在控制台看到项目监听的端口 http://127.0.0.1:8000

可以在命令中添加端口号来监听不同的端口

```bash
python manage.py runserver 8080
```

### 创建超级管理员

先执行命令在数据库中创建默认表

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

现在你可以在 [登录 | Django 站点管理员](http://127.0.0.1:8000/admin/) 中找到管理界面

### 在框架中添加应用

创建一个名字叫polls的应用

```bash
python manage.py startapp polls
```

### 创建模型

在 Django 里写一个数据库驱动的 Web 应用的第一步是定义模型 - 也就是数据库结构设计和附加的其它元数据。

在 polls/models.py 中编写以下代码

```python
from django.db import models

# Create your models here.
class Video(models.Model):
    video_name = models.CharField(max_length=100) # 视频名称
    poster_url = models.CharField(max_length=200) # 海报地址
    video_url = models.CharField(max_length=200) # 海报地址
    pub_data = models.DateTimeField("date published") # 视频发布日期

# 下面两个是官方示例中的代码
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

在 setting.py 中配置 INSTALLED_APPS 后，执行命令以修改数据库表结构

```bash
python manage.py makemigrations polls
```

在 polls/admin.py 中添加如下代码后，您可以在管理员界面中找到它

```python
from django.contrib import admin
from .models import Video

# Register your models here.
admin.site.register(Video)
```

## Scrapy爬虫

下面这个命令用于创建 Scrapy 项目，名称为 spider

```bash
scrapy startproject spider
```

在项目中编写爬虫并测试

```bash
cd spider
scrapy genspider myspider www.baidu.com
scrapy crawl myspider -o test.json # 保存结果到文件
```


