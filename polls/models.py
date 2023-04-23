from django.db import models

# Create your models here.
class Video(models.Model):
    video_name = models.CharField(max_length=100) # 视频名称
    poster_url = models.CharField(max_length=200) # 海报地址
    video_url = models.CharField(max_length=200) # 海报地址
    pub_data = models.DateTimeField("date published") # 视频发布日期


class IYF_Movie(models.Model):
    movie_name = models.CharField(max_length=100)  # 电影名
    movie_type = models.CharField(max_length=100)  # 电影类型
    movie_addr = models.CharField(max_length=200)  # 影片放映地址 这个可以作为唯一标识
    movie_time = models.CharField(max_length=50)   # 上映时间
    movie_mark = models.CharField(max_length=10)   # 电影评分
    movie_actor = models.CharField(max_length=100) # 演员表
    movie_poster = models.CharField(max_length=300)# 海报地址
