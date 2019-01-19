from django.contrib import admin

from .models import Question, Choice


# Register your models here. 注册完就能在管理页面看到数据

# 可以重排列管理员界面表单的字段的顺序
class QuestionAdmin(admin.ModelAdmin):
	fields = ['pub_date', 'question_text']

# admin.site.register(Question)
admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)