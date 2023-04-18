from django.db import models

# Create your models here.
class Video(models.Model):
    video_name = models.CharField(max_length=100) # 视频名称
    poster_url = models.CharField(max_length=200) # 海报地址
    video_url = models.CharField(max_length=200) # 海报地址
    pub_data = models.DateTimeField("date published") # 视频发布日期
