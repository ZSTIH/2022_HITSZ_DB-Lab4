import random

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from activity.models import Activity
from volunteer.models import User
from .forms import LoginForm, RegisterForm
from .models import Application, Admin


def show_activity(request):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要申请参加志愿活动，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif not request.session['is_volunteer']:
        messages.success(request, '您的身份为活动管理员，只有志愿者才能申请活动')
        return render(request, 'volunteer/index.html', locals())
    template_name = 'application/activity_list.html'
    context = {'activity_list': Activity.objects.filter(activity_state=1)}  # 只有正在招募志愿者的活动才能被申请
    return render(request, template_name, context)


def submit_application(request, activity_id):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要申请参加志愿活动，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif not request.session['is_volunteer']:
        messages.success(request, '您的身份为活动管理员，只有志愿者才能申请活动')
        return render(request, 'volunteer/index.html', locals())
    activity = get_object_or_404(Activity, activity_id=activity_id)
    user_id = request.session['user_id']

    user = User.objects.filter(user_id=user_id).first()
    new_id = str(random.randint(0, 999999999))
    old_id_list = Application.objects.values_list("application_id")
    while new_id in old_id_list:
        new_id = str(random.randint(0, 999999999))

    application = Application.objects.create(application_id=new_id, admin=activity.admin, user=user, activity=activity,
                                             application_time=timezone.now(), application_state=0,
                                             application_reason="无")
    application.save()
    messages.success(request, '申请成功，请耐心等待活动管理员审核')

    return redirect("application:show_activity")


def register(request):
    register_form = RegisterForm()
    if request.session.get('is_login', None):  # 不允许重复登录
        return render(request, 'volunteer/index.html', locals())  # 自动跳转到首页
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            admin_name = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            department = register_form.cleaned_data['department']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'application/register.html', locals())
            else:
                same_id_cus = Admin.objects.filter(admin_name=admin_name)
                # same_id_mng = StoreManager.objects.filter(manager_name=username)
                if same_id_cus:  # 用户名唯一
                    message = '用户名已经存在~请换一个'
                    return render(request, 'application/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                else:
                    new_id = str(random.randint(0, 999999999))
                    old_id_list = User.objects.values_list("user_id")
                    while new_id in old_id_list:
                        new_id = str(random.randint(0, 999999999))
                    new_cus = Admin.objects.create(admin_id=new_id, admin_name=admin_name, admin_password=password1,
                                                   department=department)
                    new_cus.save()
                    messages.success(request, '注册成功！')
                    # 自动跳转到登录页面
                    login_form = LoginForm()
                    return render(request, 'application/login.html', locals())  # 自动跳转到登录页面
    else:
        return render(request, 'application/register.html', locals())

    return render(request, 'application/register.html', locals())


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
                user_cus = Admin.objects.get(admin_name=username)
                if user_cus.admin_password == password:
                    print(username, password, user_cus.admin_name, user_cus.admin_password)
                    messages.success(request, '{}登录成功！'.format(user_cus.admin_name))
                    user_cus.save()
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.admin_id
                    request.session['username'] = user_cus.admin_name
                    request.session['is_volunteer'] = False
                    request.session['department'] = str(user_cus.department)
                    return render(request, 'volunteer/index.html', locals())
                else:
                    messages.success(request, '密码不正确')
            except:
                messages.success(request, '用户不存在')
    return render(request, 'application/login.html', locals())


def check(request):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要审核志愿活动的申请，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif request.session['is_volunteer']:
        messages.success(request, '您的身份为志愿者，只有活动管理员才能审核活动')
        return render(request, 'volunteer/index.html', locals())
    template_name = 'application/application_list.html'
    admin = Admin.objects.filter(admin_id=request.session['user_id']).first()
    context = {'application_list': Application.objects.filter(admin=admin)}
    return render(request, template_name, context)


def approve(request, application_id):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要审核志愿活动的申请，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif request.session['is_volunteer']:
        messages.success(request, '您的身份为志愿者，只有活动管理员才能审核活动')
        return render(request, 'volunteer/index.html', locals())
    application = Application.objects.filter(application_id=application_id).first()
    application.application_state = 1
    application.check_result = 1
    application.check_time = timezone.now()
    application.save()

    return check(request)


def reject(request, application_id):
    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要审核志愿活动的申请，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif request.session['is_volunteer']:
        messages.success(request, '您的身份为志愿者，只有活动管理员才能审核活动')
        return render(request, 'volunteer/index.html', locals())
    application = Application.objects.filter(application_id=application_id).first()
    application.application_state = 2
    application.check_result = 2
    application.check_time = timezone.now()
    application.save()

    return check(request)
