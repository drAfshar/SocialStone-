from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('user', 'hidden')

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user', 'post', 'hidden')

@admin.register(models.Reply)
class ReplayAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','phone')

@admin.register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display=('follower','followed')

@admin.register(models.View)
class ViewAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Hashtage)
class HashtageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Usertage)
class UsertageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.WTaged)
class WTagedAdmin(admin.ModelAdmin):
    pass

