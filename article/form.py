#引入表单类
from django import forms
from .models import Article


#写文章的表单类
class ArticleForm(forms.ModelForm):
    class Meta:
        #指明数据类型来源
        model = Article
        #定义表单所含字段
        fields = ('title', 'content', 'tags', 'avatar')
