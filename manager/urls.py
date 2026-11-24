from django.urls import path
from django.contrib.auth.views import *
from .views import *

urlpatterns = [
    path("", task_list, name="task-list"),
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="manager/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("confirm-code/", confirm_code, name="confirm-code"),
    path("tasks/new/", task_create, name="task-create"),
    path("tasks/<int:pk>/edit/", task_edit, name="task-edit"),
    path("tasks/<int:pk>/delete/", task_delete, name="task-delete"),
    path("chat/", chat, name="chat"),
]