# Generated by Django 3.0.7 on 2020-07-25 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_auto_20200723_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interactivity', models.CharField(choices=[('Unknown', 'Unknown'), ('Unspecified', 'Unspecified'), ('interactive', 'Interactive'), ('non-interactive', 'Non Interactive'), ('semi-interactive', 'Semi Interactive')], default='Unspecified', max_length=20)),
                ('planning_type', models.CharField(choices=[('Unknown', 'Unknown'), ('Unspecified', 'Unspecified'), ('spontaneous', 'Spontaneous'), ('semi-spontaneous', 'Semi Spontaneous'), ('planned', 'Planned')], default='Unspecified', max_length=20)),
                ('involvement', models.CharField(choices=[('Unknown', 'Unknown'), ('Unspecified', 'Unspecified'), ('elicited', 'Elicited'), ('non-elicited', 'Non Elicited'), ('no-observer', 'No Observer')], default='Unspecified', max_length=20)),
                ('social_context', models.CharField(choices=[('Unknown', 'Unknown'), ('Unspecified', 'Unspecified'), ('Family', 'Familiy'), ('Private', 'Private'), ('Public', 'Public'), ('Controlled environment', 'Controlled Environment'), ('Public (school)', 'Public School'), ('Community', 'Community')], default='Unspecified', max_length=30)),
                ('event_structure', models.CharField(choices=[('Unknown', 'Unknown'), ('Unspecified', 'Unspecified'), ('Monologue', 'Monologue'), ('Dialogue', 'Dialogue'), ('Multilogue', 'Multilogue'), ('Not a natural format', 'Not A Natural Format'), ('Conversation', 'Conversation')], default='Unspecified', max_length=30)),
                ('channel', models.CharField(choices=[('Unknown', 'Unknown'), ('Unspecified', 'Unspecified'), ('Face to Face', 'Face To Face'), ('Experimental setting', 'Experimental Setting'), ('Broadcasting', 'Broadcasting'), ('Telephone', 'Telephone'), ('wizard-of-oz', 'Wizard Of Oz'), ('Human-machine dialogue', 'Human Machine Dialogue'), ('Other', 'Other')], default='Unspecified', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='corpus',
            name='communication_context',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.CommunicationContext'),
        ),
    ]
