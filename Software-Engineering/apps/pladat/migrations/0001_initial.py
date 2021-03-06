# Generated by Django 3.1.5 on 2021-01-18 22:59

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PladatUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='pladatuser', serialize=False, to='auth.user')),
                ('first_name', models.CharField(help_text='First name', max_length=128)),
                ('last_name', models.CharField(help_text='Last name', max_length=128)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text='Phone number', max_length=128, region=None)),
                ('address', models.CharField(help_text='Addresss', max_length=128)),
                ('city', models.CharField(help_text='City', max_length=128)),
                ('state', models.CharField(help_text='State', max_length=128, null=True)),
                ('country', django_countries.fields.CountryField(help_text='Country', max_length=2)),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('user_type', models.IntegerField(choices=[(None, 'User type'), (0, 'Student account'), (1, 'Recruiter account')], help_text='User type')),
            ],
        ),
    ]
