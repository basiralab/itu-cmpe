# Generated by Django 3.1.5 on 2021-01-19 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pladat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pladatuser',
            name='state',
            field=models.CharField(blank=True, help_text='State', max_length=128, null=True),
        ),
    ]
