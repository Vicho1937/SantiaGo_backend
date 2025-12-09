# Generated manually for business owner system
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Agregar campos de control de propietario en Business
        migrations.AddField(
            model_name='business',
            name='created_by_owner',
            field=models.BooleanField(default=False, verbose_name='Creado por propietario'),
        ),
        migrations.AddField(
            model_name='business',
            name='status',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('draft', 'Borrador'),
                    ('pending_review', 'Pendiente de Revisión'),
                    ('published', 'Publicado'),
                    ('rejected', 'Rechazado'),
                ],
                default='published',
                verbose_name='Estado'
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='approved_by',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='approved_businesses',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Aprobado por'
            ),
        ),
        migrations.AddField(
            model_name='business',
            name='approved_at',
            field=models.DateTimeField(null=True, blank=True, verbose_name='Fecha de aprobación'),
        ),
        migrations.AddField(
            model_name='business',
            name='rejection_reason',
            field=models.TextField(blank=True, verbose_name='Razón de rechazo'),
        ),
        
        # Crear tabla BusinessOwnerProfile
        migrations.CreateModel(
            name='BusinessOwnerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_create_businesses', models.BooleanField(default=False, verbose_name='Puede crear negocios')),
                ('max_businesses_allowed', models.IntegerField(
                    default=0,
                    verbose_name='Máximo de negocios permitidos',
                    help_text='-1 para ilimitado, 0 para ninguno'
                )),
                ('is_verified_owner', models.BooleanField(default=False, verbose_name='Propietario verificado')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='owner_profile',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Perfil de Propietario',
                'verbose_name_plural': 'Perfiles de Propietarios',
                'db_table': 'business_owner_profiles',
            },
        ),
    ]
