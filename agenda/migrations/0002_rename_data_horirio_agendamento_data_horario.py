# Generated by Django 5.2.4 on 2025-07-17 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agendamento',
            old_name='data_horirio',
            new_name='data_horario',
        ),
    ]
