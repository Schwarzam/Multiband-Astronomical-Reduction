# Generated by Django 4.1.3 on 2023-04-20 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_remove_processedsci_superflatfile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=250, null=True)),
                ('flag', models.IntegerField(default=-1)),
            ],
        ),
        migrations.AddField(
            model_name='finaltiles',
            name='flag',
            field=models.IntegerField(default=-1),
        ),
    ]
