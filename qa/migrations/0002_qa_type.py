# Generated by Django 3.2.12 on 2022-05-03 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='qa',
            name='type',
            field=models.CharField(choices=[('T', 'Tips'), ('Q', 'Qa')], default='Q', max_length=1),
        ),
    ]
