from django.urls import path

from .views import show_activity, submit_application, register, login, check, approve, reject

app_name = 'application'
urlpatterns = [
    path('', show_activity, name='show_activity'),
    path('submit/<slug:activity_id>', submit_application, name='submit_application'),
    path('register/', register),
    path('login/', login),
    path('check/', check),
    path('approve/<slug:application_id>', approve, name='approve_application'),
    path('reject/<slug:application_id>', reject, name='reject_application'),
]
