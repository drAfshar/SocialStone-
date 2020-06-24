from django.contrib import admin
from django.urls import path ,re_path ,include
from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from SocialStone import settings

urlpatterns = [
    re_path("(?P<username>\w+)/$", views.profile),
    path("trend/<int:pk>", views.trend_display),
    path("follow/<int:pk>", views.follow),
    path("user/edit", views.user_edit ,name='user_edit'),
    path("upload/pic/user", views.upload_user_image, name="upic"),
    path("post/create", views.post_create, name="post_create" ),#ced=>create/edit
    path("post/<int:pk>", views.post_display, name="post_display"),
    path("post/taker/<int:pk>", views.post_taker ,name="post_taker"),
    path("post/remove/<int:pk>", views.post_remove, name="post_remove"),
    path("ajax/like/<int:pk>", views.post_like, name="post_like"),
    path("comment/like/<int:pk>", views.comment_like , name="comment_like"),
    path("comment/remove/<int:pk>", views.comment_remove, name="comment_remove"),
    path("comment/create", views.comment_create, name="comment_create"),
    path("reply/like/<int:pk>", views.reply_like , name="reply_like"),
    path("rep/create", views.reply_create, name="reply_create"),
    path("rep/edit", views.reply_edit, name="reply_edit"),
    path("rep/taker/<int:pk>", views.reply_taker, name="reply_taker"),
    path("rep/remove/<int:pk>", views.reply_remove, name="reply_remove"),
    path("file/remove/<int:pk>", views.file_remove, name="file_remove"),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)