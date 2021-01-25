# Generated by Django 3.1.5 on 2021-01-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_auto_20210120_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default='my bio', upload_to='images/'),
            preserve_default=False,
        ),
    ]
