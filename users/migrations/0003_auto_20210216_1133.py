# Generated by Django 3.1.4 on 2021-02-16 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210124_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='/static/img/user-placeholder.jpg', upload_to='profile-images/'),
        ),
    ]
