# Generated by Django 5.1.2 on 2024-12-12 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('event_category', models.CharField(choices=[('education', 'Education'), ('sport', 'Sport'), ('game', 'Game'), ('entertainment', 'Entertainment'), ('social', 'Social')], default='education', max_length=50)),
                ('about_event', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='event_images/')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('province', models.CharField(default='تهران', max_length=100)),
                ('city', models.CharField(default='تهران', max_length=100)),
                ('neighborhood', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('registration_start_date', models.DateTimeField(blank=True, null=True)),
                ('registration_end_date', models.DateTimeField(blank=True, null=True)),
                ('full_description', models.TextField()),
                ('max_subscribers', models.PositiveIntegerField()),
                ('event_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to='userapp.user')),
            ],
            options={
                'verbose_name': 'رویداد',
                'verbose_name_plural': 'رویدادها',
            },
        ),
        migrations.CreateModel(
            name='EventFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_features', to='Eventapp.event')),
            ],
            options={
                'verbose_name': 'ویژگی رویداد',
                'verbose_name_plural': 'ویژگی های رویداد',
            },
        ),
        migrations.CreateModel(
            name='UserEventRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('regular', 'Regular'), ('admin', 'Admin')], default='regular', max_length=10)),
                ('is_approved', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Eventapp.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.user')),
            ],
            options={
                'verbose_name': 'نقش کاربر در رویداد',
                'verbose_name_plural': 'نقش کاربرها در رویداد',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='subscribers',
            field=models.ManyToManyField(related_name='joined_events', through='Eventapp.UserEventRole', to='userapp.user'),
        ),
    ]
