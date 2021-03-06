# Generated by Django 3.2.12 on 2022-06-09 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=32)),
                ('title', models.CharField(default='物品丢失', max_length=64)),
                ('text', models.CharField(blank=True, default=None, max_length=256)),
                ('pic1', models.FileField(blank=True, upload_to='')),
                ('pic2', models.FileField(blank=True, upload_to='')),
                ('pic3', models.FileField(blank=True, upload_to='')),
                ('time', models.DateTimeField()),
                ('reply', models.CharField(blank=True, default=None, max_length=256)),
                ('importace', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('person', models.IntegerField()),
                ('post', models.IntegerField()),
            ],
        ),
    ]
