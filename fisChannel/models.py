from django.db import models

# Create your models here.
class tongdao(models.Model):
    ip = models.CharField(max_length=32, blank=True, null=True, verbose_name='ip地址')
    tongdaoN = models.CharField(max_length=32, blank=True, null=True, verbose_name='设备名称')
    tongdaoFull = models.CharField(max_length=32, blank=True, null=True, verbose_name='通道全称')
    description = models.CharField(max_length=32, blank=True, null=True, verbose_name='描述')
    sheetName = models.CharField(max_length=32, blank=True, null=True, verbose_name='fromSheets')
    instance = models.CharField(max_length=32, null=True, blank=True)#类似A23F12CS
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')#发送到前台
    ctime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    uptime = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='修改时间')

    tongdao_type_choices = (
        (0, '一般通道'),
        (1, '重要通道'),
    )
    tongdao_type_id = models.IntegerField(choices=tongdao_type_choices,default=0, null=True, verbose_name='通道重要程度')

    #数据库中有个一个隐藏的字段是 sb_id, 这是一个数字
    # sb 是一个对象，用于跨表查询, 代表了另外一张表的一行数据
    sb = models.ForeignKey("shebei",to_field='shebei_id',blank=True, null=True, verbose_name='设备id')#外键

    def __unicode__(self):
        return self.tongdaoN

    class Meta:
        verbose_name = '通道'
        verbose_name_plural = verbose_name
        ordering = ["tongdaoN"]   





class shebei(models.Model):
    shebei_id = models.AutoField(primary_key=True)
    factory = models.CharField(max_length=32, blank=True,  null=True, verbose_name='工厂')
    department = models.CharField(max_length=32, blank=True,  null=True, verbose_name='部门')
    shebeiN = models.CharField(max_length=32, blank=True,  null=True, verbose_name='设备名称')#不可以重复
    shebeRemarks = models.TextField(blank=True, null=True, verbose_name='设备的备注')
    
    r = models.ManyToManyField('contact', verbose_name='联系人',blank=True, null=True)
    # manytomany
    def __unicode__(self):
        return self.shebeiN

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name       
        ordering = ["shebeiN"]


class contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    contacts = models.CharField(max_length=32, blank=True,  null=True, verbose_name='联系人姓名')
    mobile = models.CharField(max_length=32, blank=True,  null=True,verbose_name='手机')
    tel = models.TextField(blank=True,  null=True, verbose_name='座机')
    email = models.CharField(max_length=32, blank=True,  null=True,verbose_name='邮箱')
    email_lower = models.CharField(max_length=32, blank=True,  null=True,verbose_name='邮箱')
    contactRemarks = models.TextField(blank=True, null=True, verbose_name='联系人的备注') 
    # manytomany



    def __unicode__(self):
        return self.contacts

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = verbose_name       
        ordering = ["contacts"]
