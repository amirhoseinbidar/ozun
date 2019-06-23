from django.contrib import admin
from .models import Answer, Question

class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline,]

admin.site.register(Answer)
admin.site.register(Question,QuestionAdmin)
