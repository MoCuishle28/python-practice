# from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("Hello, django. You're at the polls index.(中文啊！！！)")