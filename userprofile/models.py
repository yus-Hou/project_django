from django.db import models
from django.contrib.auth.models import User
#引入内置信号
from django.db.models.signals import post_save
#引入信号接收器的装饰器
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    #与User模型构成一对一关系
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #真实姓名
    name = models.CharField(max_length=10, blank=True)
    #生日
    birth = models.CharField(max_length=20, blank=True)
    #手机
    phone = models.CharField(max_length=20, unique=True, blank=True)
    #头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    #个人简介
    intro = models.CharField(max_length=500, blank=True)
    #毕业学校
    school = models.CharField(max_length=100, blank=True)
    #个人职业
    profession = models.CharField(max_length=20, blank=True)
    #个人学历
    education = models.CharField(max_length=10, blank=True)
    #个人技能
    skill = models.CharField(max_length=100, blank=True)
    #地址
    address = models.CharField(max_length=100, blank=True)
    #个人经历
    career = models.CharField(max_length=1000, blank=True)
    #社交主页
    homepage = models.CharField(max_length=50, blank=True)
    #更新时间
    update = models.DateField(auto_now=True)
    def __str__(self):
        return 'user{}'.format(self.user.username)

    class Meta:

        verbose_name = '用户信息'

#信号接收函数，每当新建User时自动调用
# @receiver(post_save, sender = User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user= instance)
#
# @receiver(post_save, sender= User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

