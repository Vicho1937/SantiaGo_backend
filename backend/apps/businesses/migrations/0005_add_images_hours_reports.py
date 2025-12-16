# Generated migration for BusinessImage, OpeningHours and Report models

import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('businesses', '0004_businessview'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image_url', models.URLField(verbose_name='URL de imagen')),
                ('thumbnail_url', models.URLField(blank=True, verbose_name='URL de miniatura')),
                ('caption', models.CharField(blank=True, max_length=255, verbose_name='Descripción')),
                ('alt_text', models.CharField(blank=True, max_length=255, verbose_name='Texto alternativo')),
                ('image_type', models.CharField(choices=[('cover', 'Portada'), ('gallery', 'Galería'), ('logo', 'Logo'), ('menu', 'Menú'), ('interior', 'Interior'), ('exterior', 'Exterior'), ('product', 'Producto')], default='gallery', max_length=20)),
                ('order', models.IntegerField(default=0, verbose_name='Orden')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activa')),
                ('is_approved', models.BooleanField(default=True, verbose_name='Aprobada')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_images', to='businesses.business')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_images', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Imagen de Negocio',
                'verbose_name_plural': 'Imágenes de Negocios',
                'db_table': 'business_images',
                'ordering': ['business', 'order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day_of_week', models.IntegerField(choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')], verbose_name='Día de la semana')),
                ('opens_at', models.TimeField(blank=True, null=True, verbose_name='Hora de apertura')),
                ('closes_at', models.TimeField(blank=True, null=True, verbose_name='Hora de cierre')),
                ('opens_at_2', models.TimeField(blank=True, null=True, verbose_name='Segunda apertura')),
                ('closes_at_2', models.TimeField(blank=True, null=True, verbose_name='Segundo cierre')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Cerrado este día')),
                ('is_24h', models.BooleanField(default=False, verbose_name='Abierto 24 horas')),
                ('notes', models.CharField(blank=True, max_length=255, verbose_name='Notas')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opening_hours', to='businesses.business')),
            ],
            options={
                'verbose_name': 'Horario de Apertura',
                'verbose_name_plural': 'Horarios de Apertura',
                'db_table': 'opening_hours',
                'ordering': ['business', 'day_of_week'],
                'unique_together': {('business', 'day_of_week')},
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_type', models.CharField(choices=[('business', 'Negocio'), ('review', 'Reseña'), ('image', 'Imagen'), ('user', 'Usuario')], max_length=20, verbose_name='Tipo de contenido')),
                ('reason', models.CharField(choices=[('spam', 'Spam o publicidad'), ('inappropriate', 'Contenido inapropiado'), ('false_info', 'Información falsa'), ('harassment', 'Acoso o bullying'), ('copyright', 'Violación de copyright'), ('fraud', 'Fraude o estafa'), ('other', 'Otro')], max_length=20, verbose_name='Razón')),
                ('description', models.TextField(verbose_name='Descripción detallada')),
                ('evidence_urls', models.JSONField(blank=True, default=list, verbose_name='URLs de evidencia')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('reviewing', 'En revisión'), ('resolved', 'Resuelto'), ('dismissed', 'Desestimado')], default='pending', max_length=20, verbose_name='Estado')),
                ('action_taken', models.CharField(blank=True, choices=[('no_action', 'Sin acción'), ('warning', 'Advertencia enviada'), ('content_removed', 'Contenido eliminado'), ('user_suspended', 'Usuario suspendido'), ('user_banned', 'Usuario baneado')], max_length=20, verbose_name='Acción tomada')),
                ('resolution_notes', models.TextField(blank=True, verbose_name='Notas de resolución')),
                ('reviewed_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de revisión')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_made', to=settings.AUTH_USER_MODEL)),
                ('business', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='businesses.business')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='businesses.businessimage')),
                ('reported_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports_received', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='reviews.review')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_reviewed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reporte',
                'verbose_name_plural': 'Reportes',
                'db_table': 'reports',
                'ordering': ['-created_at'],
            },
        ),
    ]
