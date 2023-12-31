# Generated by Django 4.0.4 on 2022-06-01 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BiasBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('masterPath', models.CharField(max_length=150, null=True)),
                ('masterThumb', models.CharField(max_length=250, null=True)),
                ('maskPath', models.CharField(max_length=250, null=True)),
                ('maskThumb', models.CharField(max_length=250, null=True)),
                ('blockStartDate', models.DateField()),
                ('blockEndDate', models.DateField()),
                ('modeavg', models.FloatField(null=True)),
                ('medianavg', models.FloatField(null=True)),
                ('noiseavg', models.FloatField(null=True)),
                ('medianrms', models.FloatField(null=True)),
                ('noiserms', models.FloatField(null=True)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('status', models.IntegerField(default=0)),
                ('isvalid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlatByFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.CharField(max_length=4)),
                ('masterPath', models.CharField(max_length=250, null=True)),
                ('maskPath', models.CharField(max_length=250, null=True)),
                ('masterThumb', models.CharField(max_length=250, null=True)),
                ('maskThumb', models.CharField(max_length=250, null=True)),
                ('blockStartDate', models.DateField()),
                ('blockEndDate', models.DateField()),
                ('modeavg', models.FloatField(null=True)),
                ('medianavg', models.FloatField(null=True)),
                ('noiseavg', models.FloatField(null=True)),
                ('medianrms', models.FloatField(null=True)),
                ('noiserms', models.FloatField(null=True)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('status', models.IntegerField(default=0)),
                ('isvalid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlatsBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockStartDate', models.DateField()),
                ('blockEndDate', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('isvalid', models.BooleanField(default=True)),
                ('flatsByFilter', models.ManyToManyField(to='files.flatbyfilter')),
            ],
        ),
        migrations.CreateModel(
            name='IndividualFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obsDate', models.DateTimeField(null=True)),
                ('field', models.CharField(max_length=30, null=True)),
                ('file_type', models.CharField(max_length=10)),
                ('exptime', models.FloatField(null=True)),
                ('band', models.CharField(max_length=4, null=True)),
                ('file_name', models.CharField(max_length=150, unique=True)),
                ('file_path', models.CharField(max_length=250)),
                ('ovfile', models.CharField(max_length=250, null=True)),
                ('ovthumb', models.CharField(max_length=250, null=True)),
                ('thumb', models.CharField(max_length=250, null=True)),
                ('modeavg', models.FloatField(null=True)),
                ('medianavg', models.FloatField(null=True)),
                ('noiseavg', models.FloatField(null=True)),
                ('medianrms', models.FloatField(null=True)),
                ('noiserms', models.FloatField(null=True)),
                ('bpmask', models.CharField(max_length=250, null=True)),
                ('processedDate', models.DateTimeField(null=True)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('status', models.IntegerField(default=0)),
                ('isvalid', models.BooleanField(default=True)),
                ('processed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='files.individualfile')),
            ],
        ),
        migrations.CreateModel(
            name='SciByFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.CharField(max_length=4)),
                ('superFlatPath', models.CharField(max_length=250, null=True)),
                ('superFlatThumb', models.CharField(max_length=250, null=True)),
                ('blockStartDate', models.DateField()),
                ('blockEndDate', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('isvalid', models.BooleanField(default=True)),
                ('processed', models.ManyToManyField(related_name='sci2proc', to='files.individualfile')),
                ('scies', models.ManyToManyField(related_name='scies', to='files.individualfile')),
            ],
        ),
        migrations.CreateModel(
            name='SciBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockStartDate', models.DateField()),
                ('blockEndDate', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('isvalid', models.BooleanField(default=True)),
                ('sciByFilter', models.ManyToManyField(to='files.scibyfilter')),
            ],
        ),
        migrations.CreateModel(
            name='ReductionBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('status', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('biasBlock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.biasblock')),
                ('flatsBlock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.flatsblock')),
                ('sciBlock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='files.sciblock')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedSci',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('individual_catalog', models.CharField(max_length=250, null=True)),
                ('superFlatFile', models.CharField(max_length=250, null=True)),
                ('superFlatThumb', models.CharField(max_length=250, null=True)),
                ('masterBiasUsed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='files.biasblock')),
                ('masterFlatUsed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='files.flatbyfilter')),
                ('scampOut', models.ManyToManyField(related_name='scamp', to='files.file')),
                ('sciraw', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='files.individualfile')),
                ('sextractorOut', models.ManyToManyField(related_name='sextr', to='files.file')),
                ('swarpOut', models.ManyToManyField(related_name='swarp', to='files.file')),
            ],
        ),
        migrations.AddField(
            model_name='individualfile',
            name='sci',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='files.processedsci'),
        ),
        migrations.AddField(
            model_name='flatbyfilter',
            name='flats',
            field=models.ManyToManyField(to='files.individualfile'),
        ),
        migrations.CreateModel(
            name='FinalTiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=30, null=True)),
                ('band', models.CharField(max_length=4, null=True)),
                ('file_path', models.CharField(max_length=250, null=True)),
                ('weight_path', models.CharField(max_length=250, null=True)),
                ('file_thumb', models.CharField(max_length=250, null=True)),
                ('weight_thumb', models.CharField(max_length=250, null=True)),
                ('modeavg', models.FloatField(null=True)),
                ('medianavg', models.FloatField(null=True)),
                ('noiseavg', models.FloatField(null=True)),
                ('medianrms', models.FloatField(null=True)),
                ('noiserms', models.FloatField(null=True)),
                ('date', models.DateField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('comments', models.CharField(max_length=300, null=True)),
                ('isvalid', models.BooleanField(default=True)),
                ('composedBy', models.ManyToManyField(to='files.individualfile')),
            ],
        ),
        migrations.AddField(
            model_name='biasblock',
            name='bias',
            field=models.ManyToManyField(to='files.individualfile'),
        ),
    ]
