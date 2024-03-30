# Generated by Django 5.0.3 on 2024-03-30 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_alter_device_current_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='current_holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.employee'),
        ),
    ]