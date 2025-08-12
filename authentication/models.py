from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminManager(BaseUserManager):
    def create_user(self, email, name, designation, password=None):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        admin = self.model(email=email, name=name, designation=designation)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, email, name, designation, password):
        return self.create_user(email, name, designation, password)

class Admin(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'designation']

    def __str__(self):
        return self.email
