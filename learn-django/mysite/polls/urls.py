'''
app中的urls.py要手动创建
还需要在root的urls.py中配置url
'''

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]