# Generated by Django 3.0.1 on 2020-12-30 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist_name', models.TextField(max_length=200)),
                ('Song_name', models.TextField(max_length=200)),
                ('album_name', models.TextField(max_length=200)),
                ('track_number', models.TextField(max_length=100)),
                ('release_date', models.TextField(max_length=100)),
                ('popularity', models.TextField(max_length=100)),
                ('songs_id', models.TextField(max_length=100)),
                ('Song_image', models.TextField(max_length=500)),
                ('Song_preview', models.TextField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]