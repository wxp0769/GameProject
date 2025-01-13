from django.db import models

# Create your models here.

class Site(models.Model):
    nid = models.AutoField(primary_key=True)
    site_url = models.CharField(verbose_name='站点域名', max_length=32)
    site_name = models.CharField(verbose_name='站点名称', max_length=64)
    logo = models.CharField(verbose_name='站点域名', max_length=32)
    title = models.CharField(verbose_name='SEO标题', max_length=64)
    description = models.CharField(verbose_name='Game Description', max_length=255)

    def __str__(self):
        return self.title

    class Game(models.Model):
        nid = models.AutoField(primary_key=True)
        title = models.CharField(verbose_name='Game Name', max_length=50)
        description = models.CharField(verbose_name='Game Description', max_length=255)
        iframeTitle= models.CharField(verbose_name='Game Name', max_length=50)
        iframeDescription= models.CharField(verbose_name='Game Description', max_length=255)
        thumbnail= models.CharField(verbose_name='Game Name', max_length=50)
        pageurl= models.CharField(verbose_name='Game Name', max_length=50)
        recommend=models.BooleanField(verbose_name='')
        create_time = models.DateTimeField(verbose_name='create_time', auto_now_add=True)
        update_time= models.DateTimeField(verbose_name='update_time', auto_now_add=True)
        content = models.TextField()
        whatis= models.TextField()
        HowtoPlay= models.TextField()
        def __str__(self):
            return self.title


