# Generated by Django 5.1.2 on 2025-01-03 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventapp', '0006_alter_comment_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usereventrole',
            name='is_approved',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
