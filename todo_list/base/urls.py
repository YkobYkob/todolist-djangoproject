from django.contrib import admin
from django.urls import path, include
from .views import TaskList, CreateTask, UpdateTask, DeleteTask, CreateUser, SigninView, SignoutView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('create-user/', CreateUser.as_view(), name='create-user'),
    path('delete-task/<int:pk>/', DeleteTask.as_view(), name='delete-task'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('update-task/<int:pk>/', UpdateTask.as_view(), name='update-task'),
]
