from django.db import models
import os
from uuid import uuid4


# Create your models here.
def get_file_path(instance, filename):
    # 将原始文件名分割为文件名和扩展名
    ext = filename.split('.')[-1]
    # 生成新的文件名，这里使用UUID确保唯一性
    filename = f"{uuid4()}.{ext}"
    # 返回文件的保存路径，这里假设我们将文件保存在'uploads/'目录下
    return os.path.join('avatars/', filename)


class Site(models.Model):
    nid = models.AutoField(primary_key=True)
    site_url = models.CharField(verbose_name='站点域名', max_length=32)
    site_name = models.CharField(verbose_name='站点名称', max_length=64)
    logo = models.FileField(upload_to=get_file_path, default="/avatars/default.png")
    title = models.CharField(verbose_name='SEO标题', max_length=64)
    description = models.CharField(verbose_name='Game Description', max_length=255)

    def __str__(self):
        return self.title

class Game(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='Game Name', max_length=50)
    description = models.CharField(verbose_name='Game Description', max_length=255)
    iframeTitle = models.CharField(verbose_name='Game Name', max_length=50)
    iframeDescription = models.CharField(verbose_name='Game Description', max_length=255)
    thumbnail = models.FileField(upload_to=get_file_path, default="/avatars/default.png")
    iframePageUrl = models.CharField(verbose_name='Play_', max_length=50)
    GamePageUrl = models.CharField(verbose_name='Game Name', max_length=50)
    recommend = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='update_time', auto_now_add=True)
    content = models.TextField()
    whatis = models.TextField()
    HowtoPlay = models.TextField()
    def __str__(self):
        return self.title
