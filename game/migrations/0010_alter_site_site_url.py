# Generated by Django 4.2.9 on 2025-01-26 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_alter_site_privacypolicy_alter_site_termofuse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='site_url',
            field=models.CharField(max_length=64, verbose_name='站点域名'),
        ),
    ]
