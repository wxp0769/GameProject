# Generated by Django 4.2.9 on 2025-02-12 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_alter_game_iframeurl_alter_site_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='answer',
            field=models.CharField(blank=True, max_length=512, verbose_name='问题答案'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='question',
            field=models.CharField(blank=True, max_length=512, verbose_name='游戏问题'),
        ),
    ]
