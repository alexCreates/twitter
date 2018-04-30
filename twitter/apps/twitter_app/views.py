from django.shortcuts import render, redirect, HttpResponse
from .models import User, Follow, Post, Inbox
from django.contrib import messages




def index(request):
    return render(request, 'twitter_app/index.html')

def show_reg(request):
    return render(request, 'twitter_app/registration.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
                return redirect('/show_reg')
        else:
            new_user = User.objects.create_user(request.POST)
            request.session['first_name'] = new_user.first_name
            request.session['last_name'] = new_user.last_name
            request.session['email'] = new_user.email
            request.session['id'] = new_user.id
            return redirect('/show')
    else:
        return render(request, 'twitter_app/registration.html')



def login(request):
    if request.method=='POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
                return redirect('/')
        else:
            logged_user = User.objects.get(email=request.POST['email'])
            request.session['first_name'] = logged_user.first_name
            request.session['last_name'] = logged_user.last_name
            request.session['email'] = logged_user.email
            request.session['id'] = logged_user.id
            return redirect('/show')
    else:
        return HttpResponse('GET method not allowed')




def show(request):
    context = {
    'all_users': User.objects.all(),
    'all_posts': Post.objects.all()
    }
    return render(request, 'twitter_app/show.html', context)



def show_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
    'first_name': user.first_name,
    'last_name': user.last_name,
    'user_id': user.id,
    'all_user_posts': Post.objects.filter(posted_by=user_id),
    'all_users_follows': User.objects.filter(is_leader = user_id)
    }
    return render(request, 'twitter_app/show_user.html', context)


def post(request, user_id):
    if request.method == 'POST':
        errors = Post.objects.validate_post(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags=tag)
                return redirect('/show')
        else:
            new_post = Post.objects.create_post(request.POST, user_id)
            return redirect('/show')
    else:
        return HttpResponse('GET method not allowed')



def follow(request, leader_id):
    errors = Follow.objects.validate_follow(request, leader_id)
    if len(errors):
        print str(errors)
        print '_' * 50
        print 'Errors are found in follow'
        print '_' * 50
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/show')
    else:
        print '_' * 50
        print 'No errors found in follow'
        print '_' * 50
        new_follow = Follow.objects.create_follow(request, leader_id)
        return redirect('/show')


def show_inbox(request, leader_id):
    context = {
    'user_of_inbox': User.objects.get(id=leader_id)
    }
    return render(request, 'twitter_app/show_inbox.html', context)


def send_message(request, leader_id, user_id):
    if request.method == 'POST':
        errors = Inbox.objects.validate_message(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, errors, extra_tags=tag)
                return redirect('/show_inbox')
        else:
            new_message = Inbox.objects.create_message(request.POST, leader_id, user_id)
            return redirect('/show_user/{}'.format(leader_id))
    else:
        return HttpResponse('GET method not allowed')


def show_user_inbox(request, user_id):
    context = {
    'user': User.objects.get(id=user_id)
    }
    return render(request, 'twitter_app/show_user_inbox.html', context)








def show_all(request):
    context = {
    'all_users': User.objects.all(),
    'all_posts': Post.objects.all(),
    'all_follows': Follow.objects.all(),
    'all_inbox': Inbox.objects.all()
    }
    return render(request, 'twitter_app/show_all.html', context)

def show_followers(request):
    leader = User.objects.get(id=request.session['id'])
    context = {
    'all_followers': User.objects.get(is_leader = leader.id).all()
    }
    return render(request, 'twitter_app/show_followers.html', context)

def delete_posts(request):
    Post.objects.all().delete()
    return redirect('/show')

def delete_follows(request):
    Follow.objects.all().delete()
    return redirect('/show')

def delete_inbox(request):
    Inbox.objects.all().delete()
    return redirect('/show')

def delete_all(request):
    User.objects.all().delete()
    Follow.objects.all().delete()
    Post.objects.all().delete()
    Inbox.objects.all().delete()
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
