from django.shortcuts import render,get_object_or_404,redirect

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from .form import CommentForm
from article.models import Article
from .models import Comment
from django.contrib.auth.models import User
from notifications.signals import notify
# Create your views here.


@login_required(login_url='/userprofile/login/')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(Article, id= article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            #二级评论
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                #若评论超过二级，强制转为二级
                new_comment.parent_id = parent_comment.get_root().id
                #被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                #给其他用户发通知
                if not parent_comment.user.is_superuser:

                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment,
                    )


                #reply接收‘200 ok’
                return JsonResponse({"code":"200 ok", "new_comment_id": new_comment.id})

            new_comment.save()
            #通知管理员
            if not request.user.is_superuser:

                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment,
                )
            #增加锚点
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)
            # 修改redirect参数
            return redirect(redirect_url)


        else:
            return HttpResponse('表单填写有误，请重试。')
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    else:
        return HttpResponse('只接受POST请求。')