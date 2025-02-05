# Generated by Django 5.1.4 on 2025-01-10 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_food'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('favorite_foods', models.ManyToManyField(blank=True, related_name='liked_by', to='bot.food')),
                ('nutrition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.foodcategory')),
            ],
        ),
    ]
