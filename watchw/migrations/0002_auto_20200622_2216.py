# Generated by Django 3.0.7 on 2020-06-22 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='main_image_url',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='product_description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='sub_image_url1',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='sub_image_url2',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(choices=[('Casual', 'Casual'), ('Dress', 'Dress'), ('Sports', 'Sports'), ('Smart', 'Smart'), ('Luxury', 'Luxury')], default=0, max_length=25),
            preserve_default=False,
        ),
    ]