# Generated by Django 3.2.8 on 2021-10-30 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='photos'),
        ),
    ]
