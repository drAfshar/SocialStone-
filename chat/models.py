from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length = 1000)
    datetime = models.DateField(auto_now_add=True)

    def last_10_messages():
        return Message.objects.order_by('-datetime')[:10].all()
    
class Room(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    joiner = models.ForeignKey(User, related_name="joiner", on_delete=models.CASCADE)
    models.DateField(auto_now_add=True)