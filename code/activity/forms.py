from django import forms

from .models import ActivityType, Location


class ActivityForm(forms.Form):
    activity_type = forms.ModelChoiceField(queryset=ActivityType.objects.all(), required=True)
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=True)
    activity_name = forms.CharField(label="活动名称", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "请填写活动名称", 'autofocus': ''}))
    activity_introduction = forms.CharField(label="活动简介", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "请填写活动简介", 'autofocus': ''}))
    activity_requirements = forms.CharField(label="活动要求", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "请填写活动要求", 'autofocus': ''}))
    activity_start_time = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    activity_end_time = forms.DateTimeField(
        input_formats=['%Y/%m/%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker2'
        })
    )
    headcount = forms.IntegerField()
