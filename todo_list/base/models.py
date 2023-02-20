from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=35, blank=False)
    description = models.TextField(max_length=120, null=True, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.title