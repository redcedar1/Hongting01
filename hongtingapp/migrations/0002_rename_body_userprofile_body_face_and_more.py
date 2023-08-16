# Generated by Django 4.2.4 on 2023-08-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hongtingapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='body',
            new_name='body_face',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='face',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='height',
            field=models.CharField(max_length=20),
        ),
    ]
