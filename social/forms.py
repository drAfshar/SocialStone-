from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from . import models


class edit_user(forms.Form):
    username = forms.CharField(required=False)
    bio = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)
    telegram = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    aparat = forms.CharField(required=False)
    youtube = forms.CharField(required=False)
    twitter = forms.CharField(required=False)

class update_userpic_form(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['image']

class post_form(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['text','image']
    id = forms.IntegerField(required=False)

class Attachment_Form(forms.ModelForm):
    class Meta:
        model = models.Attachment
        fields = ['file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text',]
    post_id= forms.IntegerField()
    comment_id = forms.IntegerField(required=False)

class reply_form(forms.Form):
    comment_id = forms.IntegerField()
    text = forms.CharField()
    username = forms.CharField(required = False)
    reply_id = forms.IntegerField(required=False)
    rep_id = forms.IntegerField(required=False)

class reply_edit_form(forms.Form):
    id = forms.IntegerField(required=False)
    text = forms.CharField(required=False)