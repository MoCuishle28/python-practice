'''
app中的urls.py要手动创建
还需要在root的urls.py中配置url
'''

from django.urls import path

from . import views


app_name = 'polls'

urlpatterns = [
	# ex: /polls/
	# path('', views.index, name='index'),
	# ex: /polls/5/  
	# template换成url标签后 可以直接在这里前面添加 specifics 修改url
	# ex: /polls/specifics/1/
	# path('specifics/<int:question_id>/', views.detail, name='detail'),
	# ex: /polls/5/results/
	# path('<int:question_id>/results/', views.results, name='results'),
	# ex: /polls/5/vote/
	path('<int:question_id>/vote/', views.vote, name='vote'),

	# 将以上的修改为使用 generic view 的形式 	( as_view()是类视图的用法 )
	path('', views.IndexView.as_view(), name='index'),
	# NOTE: question_id 改为了 pk  DetailView期望获得一个pk（会自动通过pk查找相应的数据？）
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
]