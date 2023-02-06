# Generated by Django 4.1.5 on 2023-02-06 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='promotion',
            name='type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.promotiontype'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.category'),
        ),
        migrations.AddField(
            model_name='inprocesspromo',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.product'),
        ),
        migrations.AddField(
            model_name='inprocesspromo',
            name='promotion_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.promotion'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_cat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category'),
        ),
    ]
