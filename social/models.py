from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000)
    image = models.ImageField(upload_to="social/post" ,null=True ,blank=True) 
    hidden = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return '%s,%s' % (self.user ,self.hidden )

class Comment(models.Model):
   user  = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey("Post", null=True, on_delete=models.CASCADE)
   text = models.TextField(max_length=300) 
   hidden = models.BooleanField(default=False)
   pub_date = models.DateTimeField(auto_now=True)
   updated_date = models.DateTimeField(auto_now=True)

   def __str__(self):
        return '%s,%s,%s' % (self.user ,self.post ,self.hidden)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", null=True ,blank = True , on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment",null=True ,blank=True, on_delete=models.CASCADE)
    reply = models.ForeignKey("Reply",null=True ,blank=True , on_delete=models.CASCADE)

    # def __str__(self):
    #     return '%s,%s,%s,%s' % (self.user ,self.post ,self.comment ,self.reply)


class Reply(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", null=True, on_delete=models.CASCADE) 
    text = models.TextField(max_length=300) 
    hidden = models.BooleanField(default=False) 
    reply_to_reply = models.BooleanField(default=False)
    reply_id = models.IntegerField(default=0)
    username = models.CharField(null=True ,blank=True ,max_length=100)
    pub_date = models.DateTimeField(auto_now=True) 
    updated_date = models.DateTimeField(auto_now=True) 

    #  def __str__(self):
    #         return '%s,%s,%s' % (self.user ,self.post ,self.hidden)
    
class Attachment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", null=True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='social/attachment')
    file_path = models.URLField(null=True ,blank=True)
    type_picture = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Attachment,self).delete(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="social/user")
    phone = models.CharField( max_length=20 ,null=True ,blank=True)
    address = models.TextField(max_length=300 ,null=True , blank=True)
    bio = models.TextField()
    telegram = models.URLField(max_length=500 ,blank=True)
    instagram = models.URLField(max_length=500 ,blank=True)
    aparat = models.URLField(max_length=500 ,blank=True)
    youtube = models.URLField(max_length=500 ,blank=True)
    twitter = models.URLField(max_length=500 ,blank=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return '%s,%s' % (self.user ,self.phone)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)

    def __str__(self):
        return '%s,%s' % (self.follower ,self.followed)

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    #  def __str__(self):
    #         return '%s,%s,%s' % (self.user ,self.post ,self.date)


class Hashtage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL ,null=True ,blank=True)
    post = models.ForeignKey('Post', on_delete=models.SET_NULL ,null=True ,blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.SET_NULL ,null=True ,blank=True)
    reply = models.ForeignKey('Reply', on_delete=models.SET_NULL ,null=True ,blank=True)
    tage = models.CharField(max_length=150)
    count = models.IntegerField(default=0)
    
class Usertage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE ,null=True ,blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE ,null=True ,blank=True)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE ,null=True ,blank=True)
    tage = models.CharField(max_length=150)
    seen = models.BooleanField(default=False)

class WTaged(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tage = models.CharField(max_length=150)

