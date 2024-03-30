# Generated by Django 5.0.3 on 2024-03-29 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_alter_device_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='current_holder',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.employee'),
        ),
        migrations.AlterField(
            model_name='device',
            name='assigned',
            field=models.BooleanField(default=False),
        ),
    ]