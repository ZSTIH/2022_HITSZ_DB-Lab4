import random

from django.contrib import messages
from django.shortcuts import render

from application.models import Admin
from .forms import ActivityForm
from .models import Activity


def show_activity(request):
    template_name = 'activity/activity_list.html'
    context = {'activity_list': Activity.objects.all()}
    return render(request, template_name, context)


def post_activity(request):
    activity_form = ActivityForm()

    if not request.session.get('is_login', None):
        messages.success(request, '您尚未登陆。要发布活动，请先登录')
        return render(request, 'volunteer/index.html', locals())
    elif request.session['is_volunteer']:
        messages.success(request, '您的身份为志愿者，只有活动管理员才能发布活动')
        return render(request, 'volunteer/index.html', locals())

    if request.method == "POST":
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():  # 获取数据
            new_id = str(random.randint(0, 999999999))
            old_id_list = Activity.objects.values_list("activity_id")
            while new_id in old_id_list:
                new_id = str(random.randint(0, 999999999))

            admin = Admin.objects.filter(admin_id=request.session['user_id']).first()

            activity_type = activity_form.cleaned_data['activity_type']
            activity_state = 1
            location = activity_form.cleaned_data['location']
            activity_name = activity_form.cleaned_data['activity_name']
            activity_introduction = activity_form.cleaned_data['activity_introduction']
            activity_requirements = activity_form.cleaned_data['activity_requirements']
            activity_start_time = activity_form.cleaned_data['activity_start_time']
            activity_end_time = activity_form.cleaned_data['activity_end_time']
            headcount = activity_form.cleaned_data['headcount']

            new_activity = Activity.objects.create(
                activity_id=new_id, activity_type=activity_type,
                location=location, admin=admin,
                activity_name=activity_name, activity_state=activity_state,
                activity_introduction=activity_introduction, activity_requirements=activity_requirements,
                activity_start_time=activity_start_time, activity_end_time=activity_end_time,
                headcount=headcount
            )
            new_activity.save()
            messages.success(request, '发布活动成功！')
            return show_activity(request)
        else:
            return render(request, 'activity/post_activity.html', locals())

    return render(request, 'activity/post_activity.html', locals())
