# Generated by Django 4.2.6 on 2023-10-09 05:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="products",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("m_date", models.DateTimeField(auto_created=True)),
                ("p_name", models.CharField(max_length=50)),
                ("price", models.BigIntegerField()),
                ("desc", models.TextField()),
                ("p_img", models.ImageField(upload_to="media/")),
            ],
        ),
    ]