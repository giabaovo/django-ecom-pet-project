# Generated by Django 4.2.5 on 2023-10-09 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('New', 'New'), ('Completed', 'Completed'), ('Accepted', 'Accepted')], default='New', max_length=50),
        ),
    ]
