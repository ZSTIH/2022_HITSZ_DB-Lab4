import random

from django.contrib import messages
from django.shortcuts import render

from application.models import Application
from .forms import LoginForm, RegisterForm
from .models import User


def register(request):
    register_form = RegisterForm()
    if request.session.get('is_login', None):  # 不允许重复登录
        return render(request, 'volunteer/index.html', locals())  # 自动跳转到首页
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            organization = register_form.cleaned_data['organization']
            department = register_form.cleaned_data['department']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'volunteer/register.html', locals())
            else:
                same_id_cus = User.objects.filter(username=username)
                # same_id_mng = StoreManager.objects.filter(manager_name=username)
                if same_id_cus:  # 用户名唯一
                    message = '用户名已经存在~请换一个'
                    return render(request, 'volunteer/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                else:
                    new_id = str(random.randint(0, 999999999))
                    old_id_list = User.objects.values_list("user_id")
                    while new_id in old_id_list:
                        new_id = str(random.randint(0, 999999999))
                    new_cus = User.objects.create(user_id=new_id, username=username, password=password1,
                                                  organization=organization,
                                                  department=department, total_hours=0, average_score=0)
                    new_cus.save()
                    # 自动跳转到登录页面
                    login_form = LoginForm()
                    messages.success(request, '注册成功！')
                    return render(request, 'volunteer/login.html', locals())  # 自动跳转到登录页面
    else:
        return render(request, 'volunteer/register.html', locals())

    return render(request, 'volunteer/register.html', locals())


def login(request):
    login_form = LoginForm()
    if request.session.get('is_login', None):
        return render(request, 'volunteer/index.html', locals())

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user_cus = User.objects.get(username=username)
                if user_cus.password == password:
                    messages.success(request, '{}登录成功！'.format(user_cus.username))
                    user_cus.save()
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.user_id
                    request.session['username'] = user_cus.username
                    request.session['is_volunteer'] = True
                    request.session['organization'] = str(user_cus.organization)
                    request.session['department'] = str(user_cus.department)
                    return render(request, 'volunteer/index.html', locals())
                else:
                    messages.success(request, '密码不正确')
            except:
                messages.success(request, '用户不存在')
    return render(request, 'volunteer/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return render(request, 'volunteer/index.html', locals())
    request.session.flush()
    messages.success(request, '您已成功退出登录')
    return render(request, 'volunteer/index.html', locals())


def show_info(request):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要查看个人信息，请先登录')
        return render(request, 'volunteer/index.html', locals())
    return render(request, 'volunteer/show_info.html')


def application_result(request):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要查询申请结果，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif not request.session['is_volunteer']:
        messages.success(request, '您的身份为活动管理员，只有志愿者才能查询自己的全部申请结果')
        return render(request, 'volunteer/index.html', locals())
    volunteer = User.objects.filter(user_id=request.session['user_id']).first()
    template_name = 'volunteer/application_list.html'
    context = {'application_list': Application.objects.filter(user=volunteer)}
    return render(request, template_name, context)
