# Generated by Django 4.1.2 on 2022-10-21 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0006_alter_description_certificate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="description",
            name="certificate",
            field=models.ImageField(blank=True, null=True, upload_to="description/"),
        ),
    ]
