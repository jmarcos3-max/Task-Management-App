from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def task_list(request):
    status = request.GET.get("status")
    sort_by = request.GET.get("sort_by", "due_date")

    tasks = Task.objects.all()


    # Filter by status
    if status == "complete":
        tasks = tasks.filter(completed=True)
    elif status == "incomplete":
        tasks = tasks.filter(completed=False)

    # Sort tasks
    sort_options = {
        "due_date": "due_date",
        "due_date_desc": "-due_date",
        "priority": "priority",
        "priority_desc": "-priority",
        "title": "title",
        "newest": "-id",
        "oldest": "id",
    }

    tasks = tasks.order_by(sort_options.get(sort_by, "due_date"))

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "status": status,
        "sort_by": sort_by,
    })

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.due_date = request.POST.get("due_date")
        task.priority = request.POST.get("priority")

        task.save()

        return redirect("task_list")

    return render(request, "tasks/edit_task.html", {"task": task})


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")

        if due_date == "":
            due_date = None

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
        )

        return redirect("task_list")

    return render(request, "tasks/add_task.html")


from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = not task.completed
    task.save(update_fields=["completed"])
    return redirect("task_list")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()

    return redirect("task_list")


