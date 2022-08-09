from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(unique=True,null=True)
    bio=models.TextField(null=True,blank=True)
    REQUIRED_FIELDS=[]
    

class Topic(models.Model):
    topic=models.CharField(max_length=200)
    
    def __str__(self):
        return self.topic


class Report(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    headlines=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participents=models.ManyToManyField(User,related_name="participents",blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.headlines
    
class Comment(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    Report=models.ForeignKey(Report,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.body[0:50]