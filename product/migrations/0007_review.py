# Generated by Django 4.1.5 on 2023-02-02 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_payaccount_account_number_and_more'),
        ('product', '0006_alter_inprocesspromo_promotion_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('comment', models.TextField(max_length=600)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customer')),
            ],
        ),
    ]
