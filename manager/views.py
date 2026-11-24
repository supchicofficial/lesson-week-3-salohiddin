from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
import random
from .models import Message, Task


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = request.POST.get("email")
        if not user.email:
            form.add_error(None, "Email is required.")
            return render(request, "manager/register.html", {"form": form})
        user.is_active = False
        user.save()
        code = str(random.randint(100000, 999999))
        request.session["confirm_code"] = code
        request.session["confirm_user_id"] = user.id
        send_mail(
            "Confirmation code",
            f"Your confirmation code: {code}",None,[user.email],fail_silently=False,)
        return redirect("confirm-code")
    return render(request, "manager/register.html", {"form": form})





def confirm_code(request):
    if "confirm_code" not in request.session:
        return redirect("register")
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        if code == request.session["confirm_code"]:
            user = User.objects.get(id=request.session["confirm_user_id"])
            user.is_active = True
            user.save()
            login(request, user)
            request.session.pop("confirm_code", None)
            request.session.pop("confirm_user_id", None)
            return redirect("task-list")
        return render(request, "manager/check_email.html", {"error": "Wrong code"})
    return render(request, "manager/check_email.html")




@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "manager/task_list.html", {"tasks": tasks})





@login_required
def task_create(request):
    if request.method == "POST":
        Task.objects.create(
            user=request.user,
            title=request.POST["title"],
            description=request.POST.get("description", ""),)
        return redirect("task-list")
    return render(request, "manager/task_form.html", {"task": None})





@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST.get("description", "")
        task.done = "done" in request.POST
        task.save()
        return redirect("task-list")
    return render(request, "manager/task_form.html", {"task": task})




@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task-list")
    return render(request, "manager/task_confirm_delete.html", {"task": task})




@login_required
def chat(request):
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            Message.objects.create(user=request.user, text=text)
            recipients = []
            users = User.objects.filter(is_active=True).exclude(email="")
            for user in users:
                if user != request.user:
                    recipients.append(user.email)
            if recipients:
                send_mail(
                    f"New Task Manager message from {request.user.username}",text,None,recipients,fail_silently=True,)
        return redirect("chat")
    messages = Message.objects.select_related("user").order_by("created_at")
    return render(request, "manager/chat.html", {"messages": messages})