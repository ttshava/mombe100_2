# Generated by Django 3.2.8 on 2021-10-30 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0003_alter_member_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='district_approver',
        ),
        migrations.RemoveField(
            model_name='member',
            name='overall_status',
        ),
        migrations.RemoveField(
            model_name='member',
            name='stage1_status',
        ),
        migrations.RemoveField(
            model_name='member',
            name='stage2_status',
        ),
        migrations.AddField(
            model_name='application',
            name='district_approver',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='application',
            name='overall_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='application',
            name='stage1_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='application',
            name='stage2_status',
            field=models.IntegerField(default=0),
        ),
    ]
