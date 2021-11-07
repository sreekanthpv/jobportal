from django.db import models

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
           role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user




class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    options=(
        ('jobseeker','jobseeker'),
        ('employer','employer'),
    )
    role = models.CharField(max_length=20,choices=options,default='employer')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class CompanyProfile(models.Model):
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=30)
    description=models.CharField(max_length=150)
    logo=models.ImageField(upload_to="image",null=True)

    def __str__(self):
        return self.company_name


class Jobs(models.Model):
    company=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    post_name=models.CharField(max_length=50)
    experience=models.CharField(max_length=50)
    description=models.CharField(max_length=100)

class JobSeekerProfile(models.Model):
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=40)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=150)
    resume=models.FileField(upload_to="file")

class Application(models.Model):
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    post_name=models.CharField(max_length=30,null=True)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    email=models.CharField(max_length=30,null=True)
    options=(
        ('applied','applied'),
        ('intouch','intouch'),
        ('selected','selected'),
        ('not selected','not selected'),
    )
    status=models.CharField(max_length=30,choices=options,default='applied')

