# Generated by Django 4.2.16 on 2024-11-18 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apoderado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('Jardín', 'Jardín'), ('Guardería', 'Guardería')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Niño',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField()),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=10)),
                ('apoderado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jardin_app.apoderado')),
            ],
        ),
    ]
