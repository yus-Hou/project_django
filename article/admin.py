from django.contrib import admin
from .models import Article,ArticleColumn
# Register your models here.
admin.site.site_header = '人才交流网'
admin.site.site_title = '人才交流网'

admin.site.register(Article)
admin.site.register(ArticleColumn)