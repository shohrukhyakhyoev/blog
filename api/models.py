from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        # if other_fields.get('is_staff') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username,  **other_fields)

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,**other_fields)
        user.set_password(password)
        user.save()
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150)
    # last_name = models.CharField(max_length=50)
    # member_id = models.CharField(max_length=50, unique=True)
    # start_date = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)

    # # TODO create activate account workflow to make it True
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username



class Category(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    overview = models.TextField(default='overview')
    thumbnail = models.ImageField(_("Image"))
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, related_name='tags')
    slug = models.CharField(max_length=200, default='slug')

    def __str__(self):
        return f"{self.title}"


# class Comment(models.Model):
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE) 
#     owner = models.ForeignKey(AppUser, related_name='comments', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.post} | {self.pk}"
    
    

class Project(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    thumbnail = models.ImageField(_("Image"))
    url = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=100, blank=True)
    category = models.ManyToManyField(Category, related_name='categories')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


# separate tag for academy
class Tag(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title}"
    

class Course(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    thumbnail = models.ImageField(_("Image"))
    url = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='filters')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
 