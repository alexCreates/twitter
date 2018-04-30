from __future__ import unicode_literals
from django.db import models
import re
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-A0-9._-]+\.[a-zA-Z]*$')


###########              ###########
########### - MANAGERS - ###########
###########              ###########

class InboxManager(models.Manager):
    def validate_message(self, post_data):
        errors = {}
        if len(post_data) < 1:
            errors['null'] = 'message is empty'
        return errors

    def create_message(self, clean_data, leader_id, user_id):
        new_message = Inbox.objects.create(message_content = clean_data['message_content'],
                                          sender_id = user_id,
                                          recipient_id = leader_id
                                         )
        return new_message


class PostManager(models.Manager):
    def validate_post(self, post_data):
        errors = {}
        if len(post_data['post_content']) < 1:
            errors['null'] = 'post is blank'
        return errors

    def create_post(self, clean_data, user_id):
        user = User.objects.get(id=user_id)
        return self.create(
                          post_content = clean_data['post_content'],
                          posted_by = user
                          )

class FollowManager(models.Manager):
    def validate_follow(self, request, leader_id):
        errors = {}
        follower = User.objects.get(id=request.session['id'])
        leader = User.objects.get(id = leader_id)

        f_rel_ids = follower.is_follower.all()
        l_rel_ids = leader.is_leader.all()

        result = bool(set(f_rel_ids).intersection(l_rel_ids))
        if result == True:
            errors['dup'] = 'relationship exists'
        return errors

    def create_follow(self, request, leader_id):
        logged_in_user = User.objects.get(id=request.session['id'])
        user_to_follow = User.objects.get(id=leader_id)
        return self.create(
                leader = user_to_follow,
                follower = logged_in_user
                )


class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['name']='First name must be at least two characters'
        if len(post_data['last_name']) < 2:
            errors['name']='Last name must be at least two characters'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email']='Invalid email'
        if not PASSWORD_REGEX.match(post_data['password']):
            errors['password']='Password must be at least 8 characters and have one number'
        if post_data['password'] != post_data['confirm_password']:
            errors['password']='Passwords must match'
        return errors

    def validate_login(self, post_data):
        errors = {}
        try:
            user_checker = User.objects.get(email=post_data['email'])
            if len(post_data['email']) < 1:
                errors['null'] = 'email cannot be blank'
            if len(post_data['password']) < 1:
                errors['null'] = 'password cannot be blank'
            if user_checker.password != post_data['password']:
                errors['password'] = 'invalid password'
        except User.DoesNotExist:
            if len(post_data['email']) < 1:
                errors['null'] = 'email cannot be blank'
            if len(post_data['password']) < 1:
                errors['null'] = 'password cannot be blank'
            errors['email'] = 'email does not exist'
        return errors

    def create_user(self, clean_data):
        return self.create(
        first_name = clean_data['first_name'],
        last_name = clean_data['last_name'],
        email = clean_data['email'],
        password = clean_data['password'],
        inbox = Inbox.objects.create()
        )






###########            ###########
########### - TABLES - ###########
###########            ###########
class Inbox(models.Model):
    message_content = models.TextField()
    sender_id = models.IntegerField(null=True)
    recipient_id = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = InboxManager()
    def __str__(self):
        return self.message_content, self.sender_id, self.recipient_id, self.created_at, self.updated_at

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    inbox = models.ForeignKey(Inbox, related_name = 'user_inbox')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return self.first_name, self.last_name, self.email, self.created_at, self.updated_at

class Post(models.Model):
    post_content = models.CharField(max_length = 255)
    posted_by = models.ForeignKey(User, related_name = 'posts_to_user')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PostManager()
    def __str__(self):
        return self.post_content, self.posted_by, self.created_at, self.updated_at


class Follow(models.Model):
    status = models.CharField(max_length = 255)
    leader = models.ForeignKey(User, related_name = 'is_leader')
    follower = models.ForeignKey(User, related_name = 'is_follower')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = FollowManager()
    def __str__(self):
        return self.leader, self.follower, self.created_at, self.updated_at

######## this was in validate follow ########
########           remarks           ########
# all_follow_pk_ids = Follow.objects.all().values_list('pk', flat=True)
# for loop through all_follows_ids list and check for match
# a = User.objects.all().values_list('is_leader', flat=True)
# b = objects.all().values_list('pk', flat=True)
