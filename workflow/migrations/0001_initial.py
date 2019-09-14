# Generated by Django 2.2.5 on 2019-09-12 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('quality', models.CharField(choices=[('H', 'high'), ('M', 'medium'), ('L', 'low'), ('U', 'n/a')], default='U', max_length=20)),
                ('child_speech', models.CharField(choices=[('L', 'little'), ('LN', 'little to none'), ('M', 'medium'), ('H', 'much'), ('N', 'none'), ('U', 'n/a')], default='U', max_length=30)),
                ('directedness', models.CharField(choices=[('AA', 'adult>adult'), ('AC', 'adult>child'), ('CC', 'child>child'), ('M', 'mixed'), ('N', 'none'), ('U', 'n/a')], default='U', max_length=30)),
                ('dene_speech', models.CharField(choices=[('L', 'little'), ('M', 'medium'), ('H', 'much'), ('N', 'none'), ('U', 'n/a')], default='U', max_length=30)),
                ('audio', models.CharField(blank=True, max_length=100, null=True)),
                ('length', models.DurationField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('segmentation', 'segmentation'), ('transcription', 'transcription/translation'), ('transcription check', 'check transcription/translation'), ('glossing', 'glossing'), ('glossing check', 'check glossing')], max_length=50)),
                ('status', models.CharField(choices=[('NOT-STARTED', 'not started'), ('BARRED', 'barred'), ('DEFERRED', 'deferred'), ('RESERVED', 'reserved for'), ('IN PROGRESS', 'in progress'), ('CHECKED', 'checked'), ('INCOMPLETE', 'incomplete'), ('COMPLETE', 'completed')], default='NOT-STARTED', max_length=30)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.Recording')),
            ],
            options={
                'unique_together': {('recording', 'name')},
            },
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