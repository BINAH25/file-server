# Generated by Django 4.2.10 on 2024-04-28 12:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="file",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="file",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]