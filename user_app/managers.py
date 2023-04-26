from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    # All user
    def create_user(self, username, password=None, **extra_fields):
    
        if username is None:
            raise TypeError('Users must have a username.')

        if password is None:
            raise TypeError('Users must have a password.')
    
        user = self.model(
        username = username,
        **extra_fields
        )

        # django 에서 제공하는 password 설정 함수
        user.set_password(password)
        user.save()
        
        return user