from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        create and saves a new user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        if not email:
            raise ValueError('User must have email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # impt to use this set_password function to save the user's password
        # it is a built-in function in BaseUserManager to encrypt the password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        creates a new superuser
        :param email:
        :param password:
        :return:
        """

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    custom user model that supports using email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'