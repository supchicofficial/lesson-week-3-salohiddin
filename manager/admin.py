from django.contrib import admin
from .models import Message, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "done")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "text", "created_at")
