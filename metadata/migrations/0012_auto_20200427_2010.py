# Generated by Django 2.2.5 on 2020-04-27 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0011_auto_20200414_0740'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]