# Generated by Django 4.1 on 2023-03-20 08:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0006_category_lead_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=30),
        ),
    ]
