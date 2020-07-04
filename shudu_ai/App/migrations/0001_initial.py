# Generated by Django 3.0.6 on 2020-07-04 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=64, null=True)),
                ('chemical', models.CharField(default=None, max_length=64, null=True)),
                ('distance', models.CharField(default=0, max_length=32)),
                ('detail', models.TextField(default=None, max_length=64, null=True)),
                ('audio_url', models.FilePathField()),
                ('state', models.IntegerField(default=0)),
                ('read', models.IntegerField(default=0)),
                ('time', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'audio',
            },
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=64, null=True)),
                ('img_url', models.ImageField(upload_to='')),
                ('audio', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='App.Audio')),
            ],
            options={
                'db_table': 'img',
            },
        ),
    ]
