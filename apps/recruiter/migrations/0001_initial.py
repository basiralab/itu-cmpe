# Generated by Django 3.1.5 on 2021-01-19 10:50

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pladat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('pladatuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='recruiter', serialize=False, to='pladat.pladatuser')),
                ('company_name', models.CharField(help_text='Company Name', max_length=128, null=True)),
                ('company_address', models.CharField(help_text='Company Address', max_length=128, null=True)),
                ('company_phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text='Company Phone Number', max_length=128, null=True, region=None)),
            ],
        ),
    ]
