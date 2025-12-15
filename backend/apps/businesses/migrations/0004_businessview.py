from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0003_add_owner_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=500)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_views', to='businesses.business')),
            ],
            options={
                'db_table': 'business_views',
                'ordering': ['-viewed_at'],
            },
        ),
        migrations.AddIndex(
            model_name='businessview',
            index=models.Index(fields=['business', 'viewed_at'], name='business_vi_busines_idx'),
        ),
    ]
