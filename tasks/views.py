from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Task

# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'tasks/task_form.html'
    success_url = '/'
