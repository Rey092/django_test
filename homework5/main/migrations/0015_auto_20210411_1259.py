# Generated by Django 3.1.7 on 2021-04-11 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210411_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logger',
            name='time_execution',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='logger',
            name='utm',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
