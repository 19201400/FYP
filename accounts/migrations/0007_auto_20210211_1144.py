# Generated by Django 3.0.1 on 2021-02-11 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_sentiment_records_sentiment_subjectivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='songs',
            name='popularity',
            field=models.IntegerField(max_length=100),
        ),
    ]
