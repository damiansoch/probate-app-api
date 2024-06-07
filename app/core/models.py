"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from auditlog.registry import auditlog


# region <Creating custom user model in django with extra fields name and team>
class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a superuser with the given email and password."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# endregion

# region < models>

class Agency(models.Model):
    """Agency model"""
    name = models.CharField(max_length=255)
    house_number = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    eircode = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Solicitor(models.Model):
    """Solicitor"""
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=False, max_length=255)
    phone_number = models.CharField(max_length=20)
    agency = models.ForeignKey(Agency, related_name='solicitors', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"


# endregion

auditlog.register(User)
auditlog.register(Team)
auditlog.register(Solicitor)
auditlog.register(Agency)
