# Generated by Django 4.2.6 on 2023-10-09 05:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="p_img",
            field=models.ImageField(upload_to="media"),
        ),
    ]
