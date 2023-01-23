from django.urls import path

from .views import register, login, show_info, logout, application_result

app_name = 'volunteer'
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('show_info/', show_info, name='show_info'),
    path('logout/', logout, name='logout'),
    path('application_result/', application_result),
]
