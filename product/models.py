from django.db import models

# VALIDATORS


# MODELS
class Category(models.Model):
    parent_cat = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# class Product(models.Model):
#     name = models.CharField(max_length=100, unique=True)
