# Generated by Django 4.1.5 on 2023-02-01 23:01

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_promotiontype_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='end_date',
            field=models.DateField(validators=[user.models.expiry_date_validate]),
        ),
    ]
