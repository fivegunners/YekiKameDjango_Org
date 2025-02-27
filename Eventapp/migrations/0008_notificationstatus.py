# Generated by Django 5.1.2 on 2025-01-23 12:03
# Generated by Django 5.1.2 on 2025-01-23 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventapp', '0007_alter_usereventrole_is_approved'),
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.user')),
                ('user_event_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventapp.usereventrole')),
            ],
            options={
                'unique_together': {('user', 'user_event_role')},
            },
        ),
    ]
