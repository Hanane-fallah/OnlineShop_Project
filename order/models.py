import uuid

from django.db import models

from user.models import Customer


# VALIDATORS

# MODELS
class UserCart(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_id} : {self.id}'