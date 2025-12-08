# Generated manually for profile fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_thumbnail',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='location_city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='location_state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='location_country',
            field=models.CharField(blank=True, default='Chile', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='theme_preference',
            field=models.CharField(
                choices=[('light', 'Light'), ('dark', 'Dark'), ('auto', 'Auto')],
                default='auto',
                max_length=10
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_visibility',
            field=models.CharField(
                choices=[('public', 'Public'), ('friends', 'Friends'), ('private', 'Private')],
                default='public',
                max_length=10
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='show_email',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='show_phone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='show_location',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='show_activity',
            field=models.BooleanField(default=True),
        ),
    ]
