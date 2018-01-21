from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30)
    uid = models.IntegerField()						#id+5800,直观
    assistance = models.SmallIntegerField() 		#剩余邀请次数
    cooldowntime = models.DateTimeField()			#24小时重置一次签到和邀请次数
    checkin = models.BooleanField(default=False) 				#是否签到
    ships = models.CharField(max_length=5) 			#目前拥有战舰，每一位代表一级别战舰的数量
    credits = models.PositiveIntegerField(default=0) 				#积分
    friend1 = models.IntegerField(default=0)	
    friend2 = models.IntegerField(default=0)					#不能给同一个ID助攻
    
class assistance(models.Model):
    fromuser = models.IntegerField()
    touser = models.IntegerField()
    time = models.DateTimeField(auto_now=True)