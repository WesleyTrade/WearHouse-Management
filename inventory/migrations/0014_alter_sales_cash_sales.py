# Generated by Django 5.1.6 on 2025-02-26 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_sales_overing_down_alter_sales_time_recorded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='cash_sales',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
