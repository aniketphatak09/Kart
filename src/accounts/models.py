from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email.")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)    # Also used for changing the password
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
                   email,
                   password=self.password,
                   is_staff=True
               )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
                   email,
                   password=password,
                   is_staff=True,
                   is_admin=True
               )
        return user


class User(AbstractBaseUser):
    # Fields id, password and last_login are pre-defined in AbstractBaseUser
    email = models.EmailField(unique=True, max_length=255)
    # full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff (non superuser) user
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'    # email now acts as the username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []    # ['full_name']  # these fields will be asked even when creating a superuser

    objects = UserManager()

    def __str__(self):
        return self.email

    # The following functions have to included when using a custom user model

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, object=None):
        # Does the user have a specific permission?
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Does the user have permissions to view the app `app_label`?
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class GuestModel(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
