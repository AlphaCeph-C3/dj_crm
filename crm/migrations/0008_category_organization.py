# Generated by Django 4.1 on 2023-03-20 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("crm", "0007_alter_category_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="crm.userprofile",
            ),
        ),
    ]
