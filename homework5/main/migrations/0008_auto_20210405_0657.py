# Generated by Django 3.1.7 on 2021-04-05 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210404_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.author'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=100, verbose_name='Post content'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email_to',
            field=models.EmailField(max_length=100, verbose_name='Subscriber email'),
        ),
        migrations.AlterUniqueTogether(
            name='subscriber',
            unique_together={('email_to', 'author_id')},
        ),
    ]