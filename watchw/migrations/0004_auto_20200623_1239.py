# Generated by Django 3.0.7 on 2020-06-23 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchw', '0003_auto_20200623_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]