# Generated by Django 3.1.7 on 2021-03-28 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_storage', '0004_auto_20210328_1142'),
        ('profiles', '0004_auto_20210328_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfoodstorage',
            name='date',
            field=models.DateField(auto_created=True),
        ),
        migrations.RemoveField(
            model_name='userfoodstorage',
            name='food',
        ),
        migrations.AlterField(
            model_name='userfoodstorage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_storage', to='profiles.profile'),
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='food_items', to='food_storage.foodingredient')),
            ],
            options={
                'unique_together': {('ingredient', 'quantity')},
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='daily_food',
            field=models.ManyToManyField(through='profiles.UserFoodStorage', to='profiles.FoodItem'),
        ),
        migrations.AddField(
            model_name='userfoodstorage',
            name='food',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='food_storage', to='profiles.fooditem'),
        ),
    ]
