# Generated by Django 3.0.7 on 2020-06-24 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchw', '0007_auto_20200624_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
