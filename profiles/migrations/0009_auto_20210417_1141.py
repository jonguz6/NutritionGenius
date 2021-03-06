# Generated by Django 3.1.7 on 2021-04-17 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20210410_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='calorie_goal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.FloatField(blank=True),
        ),
    ]
