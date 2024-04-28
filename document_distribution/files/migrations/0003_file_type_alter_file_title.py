# Generated by Django 4.2.10 on 2024-04-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("files", "0002_alter_file_options_file_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="type",
            field=models.CharField(default="json", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="file",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
