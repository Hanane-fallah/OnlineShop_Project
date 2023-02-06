from django.contrib.auth.models import BaseUserManager


class Usermanager(BaseUserManager):
    def create_user(self, age, mobile, first_name, last_name, username, email, password):
        if not email:
            raise ValueError('user must have email')
        if not mobile:
            raise ValueError('user must have mobile')
        if not first_name:
            raise ValueError('user must have first name')
        if not last_name:
            raise ValueError('user must have last name')

        user = self.model(username=username, first_name=first_name,
                          last_name=last_name, email=email, age=age,
                          mobile=mobile
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, age, mobile, first_name, last_name, username, email, password):
        user = self.create_user(age, mobile, first_name, last_name, username, email, password)
        user.is_staff = True
        user.save(using=self._db)
        return user
