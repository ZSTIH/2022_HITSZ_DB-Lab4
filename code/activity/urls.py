from django.urls import path

from .views import show_activity, post_activity

app_name = 'activity'
urlpatterns = [
    path('', show_activity),
    path('post_activity', post_activity)
]
