# Generated by Django 4.1.2 on 2022-10-21 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0007_alter_description_certificate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="description",
            name="certificate",
            field=models.ImageField(upload_to="description/"),
        ),
    ]
