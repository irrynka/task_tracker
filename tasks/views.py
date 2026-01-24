from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task, Comment, CommentLike
from .forms import TaskFilterForm, TaskForm, CommentForm
from .mixins import UserIsOwnerOrAuthorMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect



class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():
            status = form.cleaned_data.get('status')
            priority = form.cleaned_data.get('priority')

            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = self.object
            comment.author = request.user
            comment.save()
            return redirect('task-detail', pk=self.object.pk)
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)




class TaskUpdateView(LoginRequiredMixin, UserIsOwnerOrAuthorMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerOrAuthorMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'tasks/signup.html'
    success_url = reverse_lazy('login')


class CommentUpdateView(LoginRequiredMixin, UserIsOwnerOrAuthorMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'tasks/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})


class CommentDeleteView(LoginRequiredMixin, UserIsOwnerOrAuthorMixin, DeleteView):
    model = Comment
    template_name = 'tasks/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.task.pk})

class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            like.delete()
        return redirect('task-detail', pk=comment.task.pk)
