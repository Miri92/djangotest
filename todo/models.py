from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    author    = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title     = models.CharField(max_length = 50,verbose_name = "Title")
    completed = models.BooleanField(verbose_name = "Status")

class Shared(models.Model):
    owner       = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    #todo        = models.ForeignKey(Todo, null=True, on_delete=models.CASCADE)
    todo = models.ManyToManyField(Todo)
    
    shared_with = models.ForeignKey(
                User,
					blank=True,
					null=True,
					related_name="shared_with",
					on_delete=models.CASCADE,
					)
	
    #shared_with = models.ManyToManyField(User)
    when        = models.DateTimeField(auto_now_add=True)