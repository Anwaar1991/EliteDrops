# Generated by Django 4.2.2 on 2024-08-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_products_alibab_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
