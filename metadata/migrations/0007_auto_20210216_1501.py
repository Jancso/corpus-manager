# Generated by Django 3.1.4 on 2021-02-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_auto_20210215_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
