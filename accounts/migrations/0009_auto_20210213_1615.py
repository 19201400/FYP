# Generated by Django 3.0.1 on 2021-02-13 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210211_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songs',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
    ]