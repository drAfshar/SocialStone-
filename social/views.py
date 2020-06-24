import os
from django.shortcuts import render
from . import models
from . import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect ,JsonResponse
from django.shortcuts import render ,get_object_or_404 ,redirect
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.









def profile(request ,username ):
    user = get_object_or_404(User ,username = username)
    if user:
        profile = models.Profile.objects.get(user__username=username)
        post = models.Post.objects.filter(user__username = username).order_by('-pub_date')
        hashtages = models.Hashtage.objects.order_by('-count')[:10]
        followed = models.Follow.objects.filter(followed=user.id).exists()
        
    context = {
        'user':user ,
        'profile':profile ,
        'followed':followed ,
        'post':post,
        'hashtages':hashtages,
        }
    return render(request , 'user/profile.html' ,context)
            













def follow(request ,pk=0):
    if pk!=0:
        follower = models.Follow.objects.filter(followed = pk )
        if follower:
            follower.delete()
        else:
            #ffuser => Find Followed User
            ffuser =models.User.objects.get(id = pk)
            flw = models.Follow(follower = request.user ,followed = ffuser)
            flw.save()

        return JsonResponse(data={'state':200})













def user_edit(request):
    profile = models.Profile.objects.get(user=request.user)
    if request.method=='POST':
        form = forms.edit_user(request.POST)
        if request.POST['action']=='user_info':
            if form.is_valid():
                # request.user.username = username
                request.user.first_name = form.cleaned_data['firstname']
                request.user.last_name = form.cleaned_data['lastname']
                request.user.save()
                profile.bio = form.cleaned_data['bio']
                profile.phone = form.cleaned_data['phone']
                profile.telegram = form.cleaned_data['telegram']
                profile.aparat = form.cleaned_data['aparat']
                profile.youtube = form.cleaned_data['youtube']
                profile.instagram = form.cleaned_data['instagram']
                profile.twitter = form.cleaned_data['twitter']
                profile.address = form.cleaned_data['address']
                profile.save()
                # now change the username!
                username = form.cleaned_data['username']
                ur = models.User.objects.filter(username = username).exists()
                if ur:
                    return JsonResponse(data={'state':140, 'username':request.user.username})
                else:
                    request.user.username = username
                    request.user.save()
                return JsonResponse(data={'state':200 ,'username':request.user.username})
            
    context = {
        'profile':profile,
        }
    return render(request ,'user/edit.html' ,context)













def upload_user_image(request):
    if request.method == 'POST':
        user_profile = models.Profile.objects.get(user = request.user)
        form = forms.update_userpic_form(request.POST ,request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            if img:
                user_profile.image = img
                user_profile.save()
    return HttpResponseRedirect('/user/edit')
            













#Note : Post-create view in fact dose edit post operation too!
def post_create(request):
    if request.method=='POST':
        form= forms.post_form(request.POST, request.FILES)
        if form.is_valid():
            
            content = form.cleaned_data['text']
            img = form.cleaned_data['image']
            post_id = form.cleaned_data['id']

            if post_id !=0 :
                p = models.Post.objects.get(id=post_id)
                p.text = content
                if img:
                    p.image = img
            else:
                p = models.Post(user = request.user, hidden=False, text=content, image=img)
            p.save()

            if request.FILES:
                i=0
                for f in request.FILES.getlist('files'):
                    name ,ext = os.path.splitext(f.name)
                    if ext == '.jpg' or ext=='.png' or ext=='.mp4' and f.size <= 31457280 :
                        file = models.Attachment(file = f, user= request.user, post = p)
                        if ext == '.jpg' or ext=='.png':
                            file.type_picture = True
                        else:
                            file.type_picture = False
                        file.save()

           
            for t in p.text.split():
                if t.startswith('#'):
                    tage = models.Hashtage.objects.filter(tage=t).exists()
                    if tage:
                        tage = models.Hashtage.objects.get(tage=t)
                        tage.count = (tage.count + 1)
                    else:
                        tage = models.Hashtage(tage = t ,user = request.user ,count = 1 ,post = p)

                    wt = models.WTaged(user = request.user ,tage = t)    
                    wt.save()    
                    tage.save()
                elif t.startswith('@'):
                    tage = models.Usertage(tage = t ,user = request.user ,post = p)
                    tage.save()

                
            return JsonResponse(data = {'state':200})
        








#Post_taker (unusual)
def post_taker(request, pk):
    post = models.Post.objects.get(id=pk)
    return JsonResponse(data={'state':200 ,'text':post.text })








def post_display(request, pk):
    post = get_object_or_404(models.Post ,id=pk)
    view_checker = models.View.objects.filter(user = request.user).filter(post = post).exists()
    if view_checker==False:
        view = models.View(user = request.user ,post = post)
        view.save()
        
    views = models.View.objects.filter(post = post)
    post_like = models.Like.objects.filter(user = request.user).filter(post__id=pk)
    comment_like = models.Like.objects.filter(user = request.user)
    comment = models.Comment.objects.filter(post = post)
    replies = models.Reply.objects.filter(comment__post=post)
    hashtages = models.Hashtage.objects.order_by('-count')[:10]

    context={
        'post':post,
        'post_like':post_like,
        'comment':comment,
        'comment_like':comment_like,
        'views':views,
        'replies':replies,
        'hashtages':hashtages,
    }
    return render(request ,'post/display.html',context)
   











def post_like(request ,pk):
    post = models.Post.objects.get(id=pk)
    like_check = models.Like.objects.filter(user = request.user).filter(post = post)
    if like_check:
        like_check.delete()
        count_af = models.Like.objects.filter(post = post).count()
        return JsonResponse(data={'state':100 ,'count': count_af})
    else:      
        like = models.Like(user = request.user, post = post)
        like.save()
        count_per = models.Like.objects.filter(post = post).count()
        return JsonResponse(data={'state':200 ,'count':count_per})
    






def comment_create(request):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            comment_id = form.cleaned_data['comment_id']
            post_id = request.POST['post_id']

            if comment_id == 0:
                post = models.Post.objects.get(id = post_id)
                c = models.Comment(post = post , text = text , user = request.user , hidden=False)
            else:
                c = models.Comment.objects.get(id=comment_id)
                c.text = text
            c.save()

            for t in c.text.split():
                if t.startswith('#'):
                    tage = models.Hashtage.objects.filter(tage=t).exists()
                    if tage:
                        tage = models.Hashtage.objects.get(tage=t)
                        tage.count = (tage.count + 1)
                    else:
                        tage = models.Hashtage(tage = t ,user = request.user ,count = 1 ,comment = c)

                    wt = models.WTaged(user = request.user ,tage = t)
                    wt.save()
                    tage.save()
                elif t.startswith('@'):
                    tage = models.Usertage(tage = t ,user = request.user ,comment = c) 
                    tage.save()

            return JsonResponse(data={'state':200 ,'text':c.text})
        else:
            return JsonResponse(data={'state':100})
            










def comment_like(request, pk):
    comment = models.Comment.objects.get(id=pk)
    check_like = models.Like.objects.filter(user = request.user).filter(comment=comment)
    if check_like:
        check_like.delete()
        count = models.Like.objects.filter(comment=comment).count()
        return JsonResponse(data = {'state':100, 'count':count, 'id':pk})
    else:
        l = models.Like(user = request.user, comment = comment)
        l.save()
        count = models.Like.objects.filter(comment=comment).count()
        return JsonResponse(data = {'state':200, 'count':count, 'id':pk})













def reply_create(request):
    if request.method=='POST':
        form = forms.reply_form(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data['comment_id']
            username = form.cleaned_data['username']
            reply_id = form.cleaned_data['reply_id']
            reply = form.cleaned_data['text']

            com = models.Comment.objects.get(id = comment_id)
            r = models.Reply(user=request.user ,comment=com ,text=reply)
            if username !='' :
                rep = models.Reply.objects.get(id=reply_id)
                r.reply_to_reply= True
                r.reply_id= rep.id
                r.username = username
            r.save()

            for t in r.text.split():
                if t.startswith('#'):
                    tage = models.Hashtage.objects.filter(tage=t).exists()
                    if tage:
                        tage = models.Hashtage.objects.get(tage=t)
                        tage.count = (tage.count + 1)
                    else:
                        tage = models.Hashtage(tage = t ,user = request.user ,count = 1 ,reply = r)

                    wt = models.WTaged(user = request.user ,tage = t)
                    wt.save()
                    tage.save()
                elif t.startswith('@'):
                    tage = models.Usertage(tage = t ,user = request.user ,reply = r)
                    tage.save()
            return JsonResponse(data = {'state':200 ,'text':r.text ,'id':r.id})











def reply_edit(request):
    if request.method == 'POST':
        form = forms.reply_edit_form(request.POST)
        if form.is_valid():
            reply_id = form.cleaned_data['id']
            text = form.cleaned_data['text']
            r = models.Reply.objects.get(id = reply_id)
            r.text = text
            r.save()

            for t in r.text.split():
                if t.startswith('#'):
                    tage = models.Hashtage.objects.filter(tage=t).exists()
                    if tage:
                        tage = models.Hashtage.objects.get(tage=t)
                        tage.count = (tage.count + 1)
                    else:
                        tage = models.Hashtage(tage = t ,user = request.user ,count = 1 ,reply = r)

                    wt = models.WTaged(user = request.user ,tage = t)
                    wt.save()
                    tage.save()
                    
                elif t.startswith('@'):
                    tage = models.Usertage(tage = t ,user = request.user ,reply = r)
                    tage.save()

        return JsonResponse(data={'state':200 ,'text':r.text ,'id':r.id}) 











def reply_like(request, pk):
    reply = models.Reply.objects.get(id=pk)
    check_like = models.Like.objects.filter(user = request.user).filter(reply = reply)
    if check_like:
        check_like.delete()
        count = models.Like.objects.filter(reply = reply).count()
        return JsonResponse(data = {'state':100, 'count':count, 'id':pk})
    else:
        l = models.Like(user = request.user, reply = reply)
        l.save()
        count = models.Like.objects.filter(reply = reply).count()
        return JsonResponse(data = {'state':200, 'count':count, 'id':pk})






def reply_taker(request,pk):
    reply = models.Reply.objects.get(id=pk)
    return JsonResponse(data={'state':200, 'text':reply.text})







#Remove post attachments 
def file_remove(request ,pk):
    file = models.Attachment.objects.get(id = pk)
    file.delete()
    return JsonResponse(data={'state':200})







def post_remove(request,pk):
    post = models.Post.objects.get(id=pk)
    attachs = models.Attachment.objects.filter(post = post)
    coms = models.Comment.objects.filter(post = post)
    likes = models.Like.objects.filter()

    if attachs:
        for a in attachs:
            a.delete()

    post.delete()
    return redirect('/'+post.user.username+'/')






def comment_remove(request,pk):
    com = models.Comment.objects.get(id=pk)
    reps = models.Reply.objects.filter(comment = com)
    if reps:
        for r in reps:
            r.delete()
    com.delete()
    return JsonResponse(data={'state':200 ,'id':com.id})






def reply_remove(request,pk):
    rep = models.Reply.objects.get(id=pk)
    reps = models.Reply.objects.filter(reply_id = rep.id)
    if reps:
        for r in reps:
            r.delete()
    rep.delete()
    return JsonResponse(data={'state':200 ,'id':rep.id})







def trend_display(request, pk):
    trend = get_object_or_404(models.Hashtage ,id = pk)
    hashtages = models.Hashtage.objects.order_by('-count')[:10]
    posts = models.Post.objects.order_by('-pub_date').exclude(id = trend.id).filter(text__contains = trend.tage)



    context={
        'hashtages':hashtages,
        'trend':trend,
        'posts':posts,
    }

    return render(request, 'trend/trend_display.html', context)