
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,password=None):

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            first_name = first_name,
            last_name=last_name,
            email = email,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, first_name, last_name,email,password=None):
     
        user = self.create_user(
            first_name,
            last_name,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)   
        return user
    
class UserAccount(AbstractBaseUser,PermissionsMixin):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField(unique=True,max_length=100)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=True )
        is_superuser =models.BooleanField(default=False)
        user_image = models.ImageField(upload_to='profile',blank=True,null=True)

        objects = UserManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['first_name','last_name']




        def has_perm(self, perm, obj=None):
            return self.is_staff

        def has_module_perms(self, app_label):
            return self.is_staff

        def __str__(self):
            return self.email   
    
    