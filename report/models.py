from django.db import models

class ReportPost(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=32)
    title = models.CharField(max_length=64,default='物品丢失')
    text = models.CharField(max_length=256,default=None,blank=True)
    pic1 = models.FileField(blank=True)
    pic2 = models.FileField(blank=True)
    pic3 = models.FileField(blank=True)
    time = models.DateTimeField()
    reply = models.CharField(max_length=256,default=None,blank=True)
    reply_time = models.DateField(blank=True,null=True)
    importace = models.BigIntegerField()

class Star(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.IntegerField(blank=False)
    post = models.IntegerField(blank=False)