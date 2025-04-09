# Generated by Django 5.2 on 2025-04-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0011_alter_member_is_has_insurance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('address', models.TextField()),
                ('phone', models.TextField(blank=True, null=True)),
                ('objects_to_sell', models.IntegerField(blank=True, default=0, null=True)),
                ('objects_to_rent', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AgencyResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='New', max_length=20, null=True)),
                ('link', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='admit_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='eligible_to_practice',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='volunteer_service_history',
            field=models.JSONField(default=list),
        ),
    ]
