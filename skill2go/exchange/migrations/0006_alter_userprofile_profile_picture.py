# Generated by Django 5.1.4 on 2025-01-13 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0005_userprofile_about_me_userprofile_facebook_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='assets/default_images/default-profile.png', upload_to='profile_pics/'),
        ),
    ]
