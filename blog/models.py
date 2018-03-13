from django.db import models


# Create your models here.
class blog(models.Model):
    content = models.TextField(blank=True, null=True, verbose_name='内容')#发送到前台
    writer = models.CharField(max_length=32, blank=True, null=True, verbose_name='作者')
    ctime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    uptime = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='修改时间')

    def __unicode__(self):
        return self.tongdaoN

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ["content"]   

