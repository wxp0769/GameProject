# Generated by Django 4.2.9 on 2025-02-08 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_alter_game_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='iframeUrl',
            field=models.CharField(max_length=128, verbose_name='IFRAME'),
        ),
    ]
