import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .validators import uganda_phone_validator


class UserManager(BaseUserManager):
    """Tells Django HOW to create users and admins."""

    use_in_migrations = True

    def create_user(self, phone, full_name, password=None, **extra_fields):
        if not phone:
            raise ValueError("Users must have a phone number")
        user = self.model(phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)  # stores a hash, never the real PIN
        user.full_clean(exclude=["password"])  # runs the phone validator
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, password, **extra_fields):
        extra_fields.update(
            role=User.Role.ADMIN, is_staff=True, is_superuser=True, is_verified=True
        )
        return self.create_user(phone, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """A Kigezi Ride user: rider, driver or admin (tech doc section 7.2)."""

    class Role(models.TextChoices):
        RIDER = "rider", "Rider"
        DRIVER = "driver", "Driver"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, validators=[uganda_phone_validator])
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.RIDER)
    profile_photo = models.URLField(max_length=500, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text="Phone verified via OTP")
    is_staff = models.BooleanField(default=False, help_text="Can log in to the admin site")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"        # log in with phone instead of username
    REQUIRED_FIELDS = ["full_name"]  # asked for when creating an admin

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"
