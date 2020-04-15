from django.contrib.auth.models import User

from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse, JsonResponse
from django.views import View

from .form import UserLoginForm,UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
#用户登录
def user_login(request):
    if request.method =='POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            #.cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            #检验账号、密码是否正确匹配数据库中的某个用户
            #如果均匹配则返回这个user对象
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                #将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect('article:index')
            else:
                return HttpResponse('账号或密码有误，请重新输入。')
        else:
            return HttpResponse('账号或密码输入不合法，请检查后输入。')
    else:
        if request.method == 'GET':
            user_login_form = UserLoginForm()
            context = {'form': user_login_form}
            return render(request,'userprofile/login.html', context)
        else:
            return HttpResponse('请使用GET OR POST方法请求数据')
#用户登出
def user_logout(request):
    logout(request)
    return redirect('article:index')

# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            user_name = request.POST.get('username', '')


            u = User.objects.filter(username= user_name)


            if u:
                return HttpResponse('1')


            else:
                new_user = user_register_form.save(commit=False)
                #.cleaned_data清洗数据，将数据转换为python类型
                new_user.set_password(user_register_form.cleaned_data['password'])
                new_user.save()
                #数据保存好后进入登录状态并返回博客列表页
                login(request,new_user)
                return redirect('article:article_list')
        msg = user_register_form.errors
        return JsonResponse(msg, ensure_ascii=False)
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form':user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET OR POST方法请求数据")

def check_name(request):

    user_name = request.GET.get('username','')
    print(user_name)
    u = User.objects.filter(username=user_name).exists()
    print(u)
    print(len(user_name))
    if u:
        print("*****")
        res = {'r_link': '账号已存在'}
        return JsonResponse(res)
    elif len(user_name) >= 8 and len(user_name) <= 12:
        print("***********")

        res = {'r_link': '账号可以使用'}
        return JsonResponse(res)
    else:
        print("******")
        res = {'r_link': '账号为8-12位字符'}
        return JsonResponse(res)



def check_email(request):
    email = request.GET.get('email', '')
    e = User.objects.filter(email= email).exists()
    print(e)
    if e:
        print('****')
        res = {'r_link': '邮箱已被注册'}
        return JsonResponse(res)
    else:
        res = {'r_link':'ok'}
        return JsonResponse(res)



from .form import ProfileForm
from .models import Profile
#编辑用户信息
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user = User.objects.get(id = id)
    #user_id是 OneToOneField自动生成的字段
    # profile = Profile.objects.get(user_id= id)
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        #验证是否本人修改数据
        if request.user != user:
            return HttpResponse('你没有权限。')

        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            #取得清洗后的数据
            profile_cd = profile_form.cleaned_data

            profile.phone = profile_cd['phone']
            profile.intro = profile_cd['intro']
            profile.name = profile_cd['name']
            profile.address = profile_cd['address']
            profile.career = profile_cd['career']
            profile.education = profile_cd['education']
            profile.birth = profile_cd['birth']
            profile.homepage = profile_cd['homepage']
            profile.skill = profile_cd['skill']
            profile.school = profile_cd['school']
            profile.profession = profile_cd['profession']

            if 'avatar' in request.FILES:
                profile.avatar = profile_cd['avatar']
            profile.save()
            #返回带参的重定向
            return redirect('userprofile:userpage', id=id)
        else:
            return HttpResponse('信息输入不合法，请重新输入。')
    elif request.method =='GET':
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse('请使用GET OR POST 方法请求数据')

def check_phone(request):
    phone = request.GET.get('phone', '')
    p = Profile.objects.filter(phone=phone)
    if p:
        res = {"r_link":"手机号已被注册"}
        return JsonResponse(res ,safe=False)
    else:

        return JsonResponse('ok',safe=False)

#展示个人信息

def personal_center(request, id):

    if Profile.objects.filter(user_id=id).exists():
        print('********')
        user = User.objects.get(id=id)
        userprofile = Profile.objects.get(user=user)
        context = {'userprofile': userprofile}
        return render(request, 'userprofile/userpage.html', context)
    else:

        return redirect('userprofile:edit', id=id)



