# Generated by Django 3.2.6 on 2022-03-01 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiffine_site', '0002_auto_20220224_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='maindishmodel',
            name='type_of',
            field=models.CharField(blank=True, choices=[('veg', 'veg'), ('non_veg', 'non_veg')], max_length=10),
        ),
    ]
