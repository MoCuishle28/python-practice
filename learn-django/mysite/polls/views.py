from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question



class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	# 对于 ListView：
	# 自动生成的 context 变量是 question_list
	# 为了覆盖这个行为，我们提供 context_object_name 属性，表示我们想使用 latest_question_list
	context_object_name = 'latest_question_list'


	def get_queryset(self):
		'''
		会被自动调用 返回内容是一个集合(set)? 写上你希望在index中展示的数据是如何查询的
		返回最新的五个提问组成的集合(set)
		'''
		# 返回最近5个发布的问题（除了时间在未来的）
		return Question.objects.filter(
			# 'lte' is '<='
		    pub_date__lte = timezone.now()
		).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	# 模板中的 question 变量会自动提供，因为我们使用 Django 的模型是 Question
	template_name = 'polls/detail.html'


	def get_queryset(self):
		"""
		Excludes any questions that aren't published yet.
		排除用户直接通过url访问未来的内容
		"""
		# 'lte' is '<='  即 <= 现在时间的才能被查询到
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Question
	# 模板中的 question 变量会自动提供，因为我们使用 Django 的模型是 Question
	template_name = 'polls/results.html'
		

"""
def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = { 'latest_question_list':latest_question_list }

	# template = loader.get_template('polls/index.html')
	# return HttpResponse(template.render(context, request))

	# 以下为简易写法 参数2为返回网页相对于该应用template的相对路径
	return render(request, 'polls/index.html', context)


def detail(request, question_id):
	'''
	try:
		question = Question.objects.get(pk = question_id)
	except Exception as e:
		raise Http404('Question does not exist.')
	'''
	# 以上还可以简写为 get_object_or_404(模型对象, 条件)
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question':question} )	


def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})
"""


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
				'question':question,
				'error_message':"You didn't select a choice",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)) )