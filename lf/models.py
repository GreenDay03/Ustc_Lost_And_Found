from django.db import models
from priority import DeadlockError

# Create your models here.

class LFPost(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=32)
    date = models.DateField()
    place = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=64,default='物品丢失')
    text = models.CharField(max_length=256,default=None,blank=True)
    pic1 = models.FileField(blank=True)
    pic2 = models.FileField(blank=True)
    pic3 = models.FileField(blank=True)
    public = models.BooleanField()
    time = models.DateTimeField()
    status = models.SmallIntegerField(default=0)
    type = models.CharField(max_length=1,choices=(
        ('L', 'Lost'),
        ('F', 'Found')
    ))

class LFReply(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.IntegerField()
    author = models.CharField(max_length=32)
    text = models.CharField(max_length=256,default=None,blank=True)
    pic1 = models.FileField(blank=True)
    pic2 = models.FileField(blank=True)
    pic3 = models.FileField(blank=True)
    public = models.BooleanField()
    time = models.DateTimeField()