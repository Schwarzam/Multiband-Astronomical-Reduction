# Generated by Django 4.1.3 on 2023-06-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0020_lockedfields'),
    ]

    operations = [
        migrations.AddField(
            model_name='finaltiles',
            name='crval1',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='finaltiles',
            name='crval2',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='lockedfields',
            name='band',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
