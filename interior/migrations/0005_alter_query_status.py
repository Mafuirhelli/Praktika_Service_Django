# Generated by Django 3.2.25 on 2024-12-03 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interior', '0004_auto_20241203_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='status',
            field=models.CharField(blank=True, choices=[('n', 'Новое'), ('a', 'Принято в работу'), ('d', 'Сделано')], default='n', max_length=1),
        ),
    ]