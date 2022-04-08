# Generated by Django 3.2.12 on 2022-04-05 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userapikey',
            name='hashed_key',
            field=models.CharField(editable=False, max_length=150),
        ),
        migrations.AlterField(
            model_name='userapikey',
            name='id',
            field=models.CharField(editable=False, max_length=150, primary_key=True, serialize=False, unique=True),
        ),
    ]
