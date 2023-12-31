# Generated by Django 4.2.8 on 2023-12-14 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_changed_cover_image_field"),
    ]

    operations = [
        migrations.RemoveField(model_name="episode", name="genre",),
        migrations.RemoveField(model_name="movie", name="genre",),
        migrations.RemoveField(model_name="show", name="genre",),
        migrations.AddField(
            model_name="episode",
            name="genre",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="episodes", to="api.genre"
            ),
        ),
        migrations.AddField(
            model_name="movie",
            name="genre",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="movies", to="api.genre"
            ),
        ),
        migrations.AddField(
            model_name="show",
            name="genre",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="shows", to="api.genre"
            ),
        ),
    ]
