# Generated by Django 3.0.11 on 2021-01-01 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0002_auto_20201231_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='thing',
            name='name',
            field=models.CharField(db_index=True, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='thing',
            name='tags',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='things', to='things.Tag'),
        ),
    ]