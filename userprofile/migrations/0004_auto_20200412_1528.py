# Generated by Django 2.2 on 2020-04-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='school',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
