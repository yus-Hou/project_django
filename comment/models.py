from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey,MPTTModel

from article.models import Article
from userprofile.models import Profile


class Comment(MPTTModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name= 'comments'
    )
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= 'comments'
    )



    content = RichTextField()

    created = models.DateTimeField(auto_now_add=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ('created',)
        verbose_name_plural = '用户评论'

    def __str__(self):
        return self.content[:20]

    # class Meta:
    #