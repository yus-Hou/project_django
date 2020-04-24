from django.db import models

from django.contrib.auth.models import User
#timezone 用来处理时间相关的事务
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image
# Create your models here.

class ArticleColumn(models.Model):
    #专栏标题
    title = models.CharField(max_length=100, blank=True)
    #创建时间
    created= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '专栏'

#博客文章
class Article(models.Model):
    #on_delete 用于指定数据删除方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title  = models.CharField(max_length=100)

    content= models.TextField()

    created= models.DateTimeField(default=timezone.now)
    #文章的更新时间，auto_now=True用于指定每次更新时自动写入当前时间
    update = models.DateTimeField(auto_now=True)

    total_views = models.PositiveIntegerField(default=0)

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name= 'article'
    )

    tags = TaggableManager(blank=True)

    avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True)

    likes = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        #调用原有的 save()功能
        article = super(Article, self).save(*args,**kwargs)

        #固定宽度缩放图片
        if self.avatar and not  kwargs.get('upload_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 400
            new_y = int(new_x*(y/x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    class Meta:
        #ordering 指定模型返回数据的排列顺序
        ordering= ('-created',)
        #定义模型在数据库中的表名
        db_table= 'Article'

        verbose_name_plural = '文章'
    def __str__(self):

        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    def was_created_recently(self):
        diff = timezone.now() - self.created
        if diff.days == 0 and diff.seconds>=0 and diff.seconds<60:
            return True
        else:
            return False
