# Generated by Django 3.0.1 on 2020-12-31 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_songs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentiment_Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song_comments', models.TextField(max_length=500)),
                ('sentiment_result', models.TextField(max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('song', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Songs')),
                ('usr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
