# Generated by Django 3.1.4 on 2021-02-16 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210216_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='user-placeholder.jpg', upload_to='profile-images/'),
        ),
    ]
