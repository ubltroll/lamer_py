from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #nickname = models.CharField(max_length=30,default='username')
    uid = models.IntegerField(default=0)						#假id
    assistance = models.SmallIntegerField(default=3) 		#剩余邀请次数
    cooldowntime = models.DateTimeField(default=datetime.datetime.strptime('1815-06-18 17:41:20', '%Y-%m-%d %H:%M:%S'))			#24小时重置一次签到和邀请次数
    #checkin = models.BooleanField(default=False) 				#是否签到
    ships = models.CharField(max_length=5) 			#目前拥有战舰，每一位代表一级别战舰的数量
    credits = models.PositiveIntegerField(default=0) 				#积分
    friend1 = models.IntegerField(default=0)	
    friend2 = models.IntegerField(default=0)					#不能给同一个ID助攻
    today = models.IntegerField(default=0)
    mark = models.IntegerField(default=0)
    
class assistance(models.Model):
    fromuser = models.IntegerField()
    touser = models.IntegerField()
    time = models.DateTimeField(auto_now=True)

class setting(models.Model):
    keyword = models.CharField(max_length=30)
    value = models.IntegerField(default=0)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,uid=instance.id)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()