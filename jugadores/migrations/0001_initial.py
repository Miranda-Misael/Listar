# Generated by Django 4.2.6 on 2023-10-22 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apodo', models.CharField(max_length=30)),
                ('div', models.CharField(max_length=3)),
                ('DU', models.IntegerField(null=True)),
                ('entrena', models.BooleanField(default=True, null=True)),
                ('ImagenCampo', models.CharField(blank=True, max_length=200, null=True)),
                ('socio', models.BooleanField(default=False, null=True)),
                ('Fichaje', models.BooleanField(default=False, null=True)),
                ('fechaAct', models.DateTimeField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('nombre', models.CharField(blank=True, max_length=30, null=True)),
                ('apellido', models.CharField(blank=True, max_length=30, null=True)),
                ('fechaNaci', models.DateTimeField(blank=True, null=True)),
                ('colegio', models.CharField(blank=True, max_length=30, null=True)),
                ('domicilio', models.CharField(blank=True, max_length=30, null=True)),
                ('barrio', models.CharField(blank=True, max_length=30, null=True)),
                ('imgOS', models.CharField(blank=True, max_length=200, null=True)),
                ('imgDU', models.CharField(blank=True, max_length=200, null=True)),
                ('hnosOtraDiv', models.CharField(blank=True, max_length=30, null=True)),
                ('antecedMed', models.TextField(blank=True, max_length=200, null=True)),
                ('pracOtroDep', models.CharField(blank=True, max_length=30, null=True)),
                ('celJug', models.IntegerField(blank=True, default=0, null=True)),
                ('nombPadre', models.CharField(blank=True, max_length=30, null=True)),
                ('telPadre', models.IntegerField(blank=True, default=0, null=True)),
                ('nombMadre', models.CharField(blank=True, max_length=30, null=True)),
                ('telMadre', models.IntegerField(blank=True, default=0, null=True)),
                ('nombTutor', models.CharField(blank=True, max_length=30, null=True)),
                ('telTutor', models.IntegerField(blank=True, default=0, null=True)),
                ('Puesto', models.IntegerField(blank=True, default=0, null=True)),
                ('PuestAlt', models.IntegerField(blank=True, default=0, null=True)),
                ('puestElejJug', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]