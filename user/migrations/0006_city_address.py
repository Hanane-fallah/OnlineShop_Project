# Generated by Django 4.1.5 on 2023-02-01 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customer_mobile_alter_customer_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=9)),
                ('detail', models.TextField(max_length=300)),
                ('is_default', models.BooleanField()),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.city')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customer')),
            ],
        ),
    ]
