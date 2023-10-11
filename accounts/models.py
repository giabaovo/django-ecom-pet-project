from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField

class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError("User must have email")
        
        if not username:
            raise ValueError("User must have a nick name")
        
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = AccountManager()

    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    USERNAME_FIELD = "email" 

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=255)
    address_line_2 = models.CharField(blank=True, max_length=255)
    profile_picture = models.ImageField(upload_to="photos/user_profile", blank=True)
    country = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return "{} {}".format(self.address_line_1, self.address_line_2)
