# Generated by Django 5.1.6 on 2025-02-28 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_alter_sales_options_remove_sales_overing_down_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sales',
            options={'permissions': [('can_add_sales', 'Can add sales'), ('can_edit_sales', 'Can edit sales'), ('can_delete_sales', 'Can delete sales')]},
        ),
    ]
