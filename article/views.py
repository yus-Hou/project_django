import markdown
from django.shortcuts import render, redirect,HttpResponse
from django.utils import timezone
from django.views import View

from comment.form import CommentForm
from .form import ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Article,ArticleColumn
from comment.models import Comment

from django.db.models import Q






def article_index(request):
    #取出所有文章
    #根据GET请求中查询条件返回使用不同排序方法的对象




    article_list = Article.objects.all()


    news = article_list.order_by('-created')[0]

    hot = article_list.order_by('-total_views')[0]

    admincol = article_list.filter(column_id=5)[0]

    adminnews = article_list.filter(column_id=6)[0]

    indexnews = article_list.filter(column_id=6)

    # paginator = Paginator(article_list, 5)
    # #获取url中的页码
    # page = request.GET.get('page')
    # #将导航对象相应的页码内容返回articles
    # articles = paginator.get_page(page)
    articles = article_list.filter(
        Q(column_id=5)|
        Q(column_id=6)
    )
    #需要传递给模板的上下文
    context  = {'articles':articles, 'news': news, 'hot': hot, 'admincol': admincol, 'adminnews':adminnews, 'indexnews': indexnews}
    #render函数将上下文加载进模板
    return render(request, 'article/index.html', context)


#文章列表
def article_list(request):
    #取出所有博客
    #根据GET请求中查询条件返回使用不同排序方法的对象
    order  = request.GET.get('order')
    search = request.GET.get('search')
    column = request.GET.get('column')
    tag    = request.GET.get('tag')

    article_list = Article.objects.exclude(column_id=6)

    if search:

        article_list = Article.objects.filter(
                Q(title__icontains=search)|
                Q(content__icontains=search)
            )

    else:
        #将search参数置空
        search = ''

    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    if tag and tag!= 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    if column is not  None and column.isdigit():
        article_list = article_list.filter(column=column)


    #设置分页，每页显示一篇文章
    paginator = Paginator(article_list, 5)
    #获取url中的页码
    page = request.GET.get('page')
    #将导航对象相应的页码内容返回articles
    articles = paginator.get_page(page)


    #需要传递给模板的上下文
    context  = {'articles':articles, 'order': order, 'search': search, 'tag': tag, 'column':column,}
    #render函数将上下文加载进模板
    return render(request, 'article/list.html', context)


#文章详情
def article_detail(request, id):
    #获取相应id的文章
    article = get_object_or_404(Article, id=id)

    #取出评论
    comment = Comment.objects.filter(article = id)



    #浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    #赋给上下文变量
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])
    article.content = md.convert(article.content)
    comment_form = CommentForm()
    context = {'article': article, 'toc':md.toc, 'comments': comment, 'comment_form': comment_form,}

    return render(request, 'article/detail.html', context)

#添加文章
@login_required(login_url='/userprofile/login/')
def article_create(request):
    #判断用户是否提交数据

    if request.method == 'POST':
        #将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(request.POST,request.FILES)
        #判断提交的数据是否满足模型要求
        if article_post_form.is_valid():

            #保存数据但不提交到数据库中
            new_article = article_post_form.save(commit=False)
           
            new_article.author = User.objects.get(id= request.user.id)
            #将文章保存进数据库
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id = request.POST['column'])
            new_article.save()

            article_post_form._save_m2m()
            #返回至文章列表
            return redirect('article:article_list')
        else:
            #返回错误信息
            return HttpResponse('表单内容有误，添加失败。')
    #如果用户请求获取数据
    else:
        #创建表单实例
        article_post_form = ArticleForm()
        columns = ArticleColumn.objects.exclude(
            Q(title='站点公告')|
            Q(title='最新资讯'))
        admincols = ArticleColumn.objects.all()


        #赋值上下文
        context = {'article_post_form': article_post_form, 'columns': columns, 'admincols' : admincols}
        #返回空表单
        return render(request, 'article/create.html', context)

#删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    # #取出数据
    # article = Article.objects.get(id=id)
    # #删除数据
    # article.delete()
    # return redirect('article:article_list')
    user = User.objects.get(id = request.user.id)
    if request.method == 'POST':
        if request.user == user:
            article = Article.objects.get(id=id)
            article.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse('你没有该权限。')
    else:
        return HttpResponse('仅允许post请求')

#修改文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = Article.objects.get(id =id)
    if request.user != article.author:
        return HttpResponse('您没有该权限。')
    #判断是否为POST请求
    if request.method == 'POST':
        #将提交的数据赋给表单实例
        article_post_form = ArticleForm(data=request.POST)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.content = request.POST['content']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id = request.POST['column'])
            else:
                article.column = None
            #获取旧图
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')

            #更新tags
            article.tags.set(*request.POST.get('tags').split(','), clear= True)

            article.save()
            #重定向到文章详情
            return redirect('article:article_detail' ,id = id)
        else:
            return HttpResponse('表单内容有误，添加失败。')
    #如果用户GET请求数据
    else:
        #创建表单实例
        article_post_form = ArticleForm()
        columns = ArticleColumn.objects.all()
        #将article文章对象也传进上下文，用于提取旧数据
        context = {'article':article,
                   'article_post_form':article_post_form,
                   'columns': columns,
                   #获取tagsname
                   'tags':','.join([x for x in article.tags.names()]),

                   }
        #返回模板
        return render(request, 'article/update.html', context)


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')

