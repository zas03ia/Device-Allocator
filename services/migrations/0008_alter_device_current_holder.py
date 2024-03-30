# Generated by Django 5.0.3 on 2024-03-29 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_device_current_holder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='current_holder',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.employee'),
        ),
    ]
