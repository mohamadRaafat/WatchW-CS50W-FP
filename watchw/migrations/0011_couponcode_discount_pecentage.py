# Generated by Django 3.0.7 on 2020-06-26 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchw', '0010_couponcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcode',
            name='discount_pecentage',
            field=models.DecimalField(decimal_places=2, default=0.1, max_digits=4),
            preserve_default=False,
        ),
    ]
