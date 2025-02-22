import os
from uuid import uuid4
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.text import slugify

# Create your models here.
def get_file_path(instance, filename):
    # 将原始文件名分割为文件名和扩展名
    ext = filename.split('.')[-1]
    # 生成新的文件名，这里使用UUID确保唯一性
    filename = f"{uuid4()}.{ext}"
    # 返回文件的保存路径，这里假设我们将文件保存在'uploads/'目录下
    return os.path.join('uploads/', filename)


class Site(models.Model):
    nid = models.AutoField(primary_key=True)
    site_url = models.CharField(verbose_name='站点域名', max_length=64)
    site_name = models.CharField(verbose_name='站点名称', max_length=128)
    logo = models.ImageField(upload_to=get_file_path)
    title = models.CharField(verbose_name='SEO标题', max_length=128)
    description = models.CharField(verbose_name='站点描述', max_length=512)
    aboutus = RichTextUploadingField(verbose_name='关于我们', blank=True, null=True)
    copyright = RichTextUploadingField(verbose_name='copyright', blank=True, null=True)
    contactus = RichTextUploadingField(verbose_name='contact us', blank=True, null=True)
    Privacypolicy = RichTextUploadingField(verbose_name='Privacy policy', blank=True, null=True)
    Termofuse = RichTextUploadingField(verbose_name='Term of use', blank=True, null=True)
    games = models.ManyToManyField('Game', related_name='sites', blank=True, verbose_name='关联游戏')  # 多对多关系
    def __str__(self):
        return self.title


class Game(models.Model):
    RECOMMEND_CHOICES = [
        (0, '[0]不推荐'),
        (1, '[1]左边推荐'),
        (2, '[2]右边推荐'),
        (3, '[3]主游戏'),
        (4, '[4]顶部推荐'),
    ]
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='游戏名称', max_length=64)
    slug = models.SlugField(verbose_name='游戏网址', max_length=200, unique=True, blank=True, null=True)
    description = models.CharField(verbose_name='游戏描述', max_length=1024)
    # iframePageTitle = models.CharField(verbose_name='iframeTitle', max_length=50)
    # iframeDescription = models.CharField(verbose_name='iframeDescription', max_length=255)
    thumbnail = models.FileField(verbose_name='游戏图片', upload_to=get_file_path, default="/uploads/logo.png")
    # GamePageUrl = models.CharField(verbose_name='GamePageUrl', max_length=50)
    iframeUrl = models.CharField(verbose_name='IFRAME', max_length=512)
    recommend = models.IntegerField(choices=RECOMMEND_CHOICES, default=0, verbose_name='推荐等级')  # 默认0，1为左边，2为右边，3为首页主游戏
    create_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='update_time', auto_now_add=True)
    content = RichTextUploadingField(blank=True, null=True)
    whatis = RichTextUploadingField(blank=True, null=True)
    HowtoPlay = RichTextUploadingField(blank=True, null=True)
    source=models.CharField(verbose_name='游戏来源', max_length=128,default="")
    is_checked = models.BooleanField(verbose_name='是否发布', default=False)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Questions(models.Model):
    nid = models.AutoField(primary_key=True)
    question = models.CharField(verbose_name='游戏问题', max_length=512, blank=True)
    answer = models.CharField(verbose_name='问题答案', max_length=512, blank=True)
    game = models.ForeignKey(verbose_name='所属游戏', to='Game', to_field='nid', on_delete=models.CASCADE, null=True,
                             blank=True)

class Pachong(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='游戏名称', max_length=64,blank=True, null=True)
    description = models.TextField(verbose_name='游戏描述', max_length=512,blank=True, null=True)
    source=models.CharField(verbose_name='游戏来源', max_length=128,blank=True, null=True)
    is_caiji = models.BooleanField(verbose_name='是否已采集', default=False)
    is_publish = models.BooleanField(verbose_name='是否已发布', default=False)
