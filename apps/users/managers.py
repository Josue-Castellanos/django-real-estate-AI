from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def email_validators(self, email):
        try:
            validate_email(email)
        except ValidationError:
            return ValueError(_('Invalid email address, provide a valid email address.'))
        
    def create_user(self, username, first_name, last_name, email, password,**efs):
        if not username:
            raise ValueError(_('Users must submit a username'))
        
        if not first_name:
            raise ValueError(_('Users must submit a first name'))
        
        if not last_name:
            raise ValueError(_('Users must submit a last name'))
        
        if email:
            email = self.normalize_email(email)
            self.email_validators(email)
        else:
            raise ValueError(_('Base User Account: An email address is required'))
        
        user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **efs)

        user.set_password(password)
        efs.setdefault("is_staff", False)
        efs.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, first_name, last_name, email, password, **efs):
        efs.setdefault("is_staff", True)
        efs.setdefault("is_superuser", True)
        efs.setdefault("is_active", True)

        if efs.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))

        if efs.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))
        
        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validators(email)
        else:
            raise ValueError(_('Admin Account: An email address is required'))
        
        user = self.create_user(username, first_name, last_name, email, password, **efs)
        user.save(using=self._db)
        return user