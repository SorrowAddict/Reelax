# Generated by Django 4.2.6 on 2024-11-25 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('movies', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_actors',
            field=models.ManyToManyField(related_name='liked_by_users', to='movies.actor'),
        ),
        migrations.AddField(
            model_name='user',
            name='liked_directors',
            field=models.ManyToManyField(related_name='liked_by_users', to='movies.director'),
        ),
        migrations.AddField(
            model_name='user',
            name='liked_genres',
            field=models.ManyToManyField(related_name='liked_by_users', to='movies.genre'),
        ),
        migrations.AddField(
            model_name='user',
            name='liked_movies',
            field=models.ManyToManyField(related_name='liked_by_users', to='movies.movie'),
        ),
        migrations.AddField(
            model_name='user',
            name='playlists',
            field=models.ManyToManyField(related_name='user_playlists', to='movies.playlist'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
