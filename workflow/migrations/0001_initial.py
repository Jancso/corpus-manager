# Generated by Django 2.2.5 on 2020-03-08 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('metadata', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('segmentation', 'segmentation'), ('transcription', 'transcription/translation'), ('glossing', 'glossing')], max_length=50)),
                ('status', models.CharField(choices=[('NOT-STARTED', 'not started'), ('BARRED', 'barred'), ('DEFERRED', 'defer'), ('RESERVED', 'reserved for'), ('IN PROGRESS', 'in progress'), ('CHECKED', 'CHECK'), ('INCOMPLETE', 'incomplete'), ('COMPLETE', 'complete'), ('NO MEDIA', 'no media'), ('PROBLEMS', 'problems'), ('UNCLEAR', 'UNCLEAR')], default='NOT-STARTED', max_length=30)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.Recording')),
            ],
            options={
                'unique_together': {('recording', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recordings', models.ManyToManyField(to='metadata.Recording')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Discussion')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Task')),
            ],
            options={
                'unique_together': {('task', 'person')},
            },
        ),
    ]
