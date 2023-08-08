from django.db import models
from django.contrib.auth.models import User



class CustomUser(User):
    avatar =  models.CharField(max_length=150, default="") 

    friends = models.ManyToManyField('self')  
    session_data_backup = models.TextField(default='')


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200, default="")

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)  

#HW8 Comment model 
class Comment(models.Model):
    body = models.CharField(max_length=200)  
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)




# models        -> field types, relations
# models.Model  -> ORM