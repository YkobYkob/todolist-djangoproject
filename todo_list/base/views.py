from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.middleware.csrf import get_token

from .models import Task

class CustomUserCreationForm(UserCreationForm): #Editing the built-in UserCreationForm (changing the max length of username)
    username = forms.CharField(max_length=15)

class CreateUser(FormView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'base/signup.html'
    success_url = reverse_lazy('tasks')
    redirect_authenticated_user = True


    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(CreateUser, self).form_valid(form)
    

    def form_invalid(self, form):
        message = ''
        username = self.request.POST.get('username')

        if User.objects.filter(username=username).exists(): #Checking if the username does already exist
            message = 'This username is already taken. Please choose another one.'
        return render(self.request, self.template_name, {'form': form, 'error_message': message})

    
    

class SigninView(LoginView):
    model = User
    fields = '__all__'
    redirect_authenticated_user = True
    template_name = 'base/signin.html'

    def get_success_url(self):
        return reverse_lazy('tasks')
    
    

class SignoutView(LogoutView, LoginRequiredMixin):
    model = User
    def get_success_url(self):
        return reverse_lazy('tasks')



class TaskList(ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs): #For only showing the tasks created by the logged in user
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            context['tasks'] = Task.objects.filter(user=self.request.user)
            return context
    
    def post(self, request, *args, **kwargs): #Making the TaskList class-based view able to handle POST requests
        # Handle the POST request
        return JsonResponse({'status': 'success'})
    
    def get_context_data(self, **kwargs): #Giving this view a csrf_token, despite this view only being for GET requests.
        context = super().get_context_data(**kwargs)
        context['csrf_token'] = get_token(self.request)
        return context
    
    def post(self, request): #AJAX POST request reciever
        task_id = request.POST['task_id']
        completed = request.POST['completed']
        task = Task.objects.get(pk=task_id)
        task.completed = (completed == 'true')
        task.save()
        return JsonResponse({'success': True})



class CreateTask(CreateView, LoginRequiredMixin):
    model = Task
    template_name = 'base/create-task.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(UpdateView, LoginRequiredMixin):
    model = Task
    template_name = 'base/update-task.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')



class DeleteTask(DeleteView, LoginRequiredMixin):
    model = Task
    template_name = 'base/delete-task.html'
    success_url = reverse_lazy('tasks')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)