from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, name, email, mood, password=None, active=True, staff=False, admin=False, verified=False):
        if not email:
            raise ValueError("Users must have an email address")

        if not password:
            raise ValueError("Users must have password")

        user_obj = self.model(
            name=name,
            mood=mood,
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.is_staff = staff
        user_obj.is_admin = admin
        user_obj.is_active = active
        user_obj.is_verified = verified
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, name, email, mood, password=None):
        user = self.create_user(
            name,
            email,
            mood="happy",
            password=password,
            staff=True
        )

        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(
            name,
            email,
            mood="happy",
            password=password,
            staff=True,
            admin=True
        )
        user.is_superuser = True
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=50, blank=True)
    mood = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }