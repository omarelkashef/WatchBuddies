# Generated by Django 4.2.8 on 2023-12-22 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_buddiesinvite_responded_groupinvite_responded_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="buddiesinvite", unique_together=set(),),
    ]
