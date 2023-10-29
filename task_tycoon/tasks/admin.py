from django.contrib import admin
from .models import Task, Question, Answer, Settings

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'identifier', 'creator', 'slug', 'upload')
    list_display_links = ('id', 'identifier')
    search_fields = ('title', 'identifier', )
    list_editable = ('title', )
    list_filter = ('creator', )
    prepopulated_fields = {'slug': ('title',)}


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'test_type', 'task', 'variants')
    list_display_links = ('id', )
    search_fields = ('title', )
    list_editable = ('title', 'variants')
    list_filter = ('test_type', 'task')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'content')
    list_display_links = ('id', )
    search_fields = ('user', 'task')
    list_editable = ('content', )
    list_filter = ('user', 'task')


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'feedback', 'attempts')
    list_display_links = ('id', )
    search_fields = ('task', )
    list_editable = ('feedback', 'attempts')
    list_filter = ('feedback', )


admin.site.register(Task, TaskAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Settings, SettingsAdmin)
