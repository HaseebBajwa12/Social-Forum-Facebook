from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def upload_profiles(instance, filename):
    return "profiles/{filename}".format(filename=filename)


def upload_cover_image(instance, filename):
    return "cover_images/{filename}".format(filename=filename)


class CustomAccountManager(BaseUserManager):
    """Custom Account Manager class.
    Parameters
    ----------
    BaseUserManager : django.contrib.auth.models
    """

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        """Create django super user.
        Parameters
        ----------
        email : str
        first_name : str
        last_name : str
        password : str
        Returns
        -------
        django.contrib.auth.models import User
        Raises
        ------
        ValueError
            raise "Superuser must be assigned to is_staff=True." if user has not staff role
        ValueError
            raise "Superuser must be assigned to is_superuser=True." if user has not superuser role
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, username, first_name, last_name, password, **other_fields)

    def create_user(self, email, username, first_name, last_name, password, **other_fields):
        """Create django super user.
        Parameters
        ----------
        email : str
        first_name : strrror: could not apply f375edd... admin panel customizat
        last_name : str
        password : str
        username: str
        Returns
        -------
        django.contrib.auth.models.User
        Raises
        ------
        ValueError
            raise "You must provide an email address" if email address is not given
        """
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Django core user class.
    Parameters
    ----------
    AbstractBaseUser : django.contrib.auth.models
    PermissionsMixin : django.contrib.auth.models
    Returns
    -------
    django.contrib.auth.models.User
    """

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(
        max_length=250,
        unique=True,
        help_text=("Required. 250 characters or fewer. Letters, and digits only."),
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    dob = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        """Str representation of user accounts.
        Returns
        -------
        str
            returns the string containing the first name and last name
        """
        return f"{self.first_name} {self.last_name}"


class Profile(models.Model):
    profile_image = models.ImageField(
        _("profiles"), upload_to=upload_profiles, default="profiles/default.png", blank=True, null=True
    )

    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    cover_image = models.ImageField(
        _("cover_Image"), upload_to=upload_cover_image, default="cover_images/cover.png", blank=True, null=True
    )
    bio = models.CharField(blank=True, max_length=255)
    choices = [("male", "Male"), ("female", "Female"), ("other", "Others")]
    gender = models.CharField(max_length=6, choices=choices)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def __str__(self):
        """Str representation of user accounts.
        Returns
        -------
        str
            returns the string containing the first name and last name
        """
        return f"{self.user}"
