# Generated by Django 4.1.3 on 2023-06-20 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0021_finaltiles_crval1_finaltiles_crval2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lockedfields',
            name='field',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
