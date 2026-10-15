from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.db.models import Q

def task_list(request):
    tasks = Task.objects.all()
    query = request.GET.get("q")

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "query": query
    })

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.save()

        return redirect("task_list")

    return render(request, "tasks/edit_task.html", {"task": task})


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Task.objects.create(
            title=title,
            description=description
        )

        return redirect("task_list")

    return render(request, "tasks/add_task.html")    
   
