# Generated by Django 3.1.7 on 2021-03-28 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210328_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='daily_food',
            field=models.ManyToManyField(related_name='daily_food', through='profiles.UserFoodStorage', to='profiles.FoodItem'),
        ),
    ]
