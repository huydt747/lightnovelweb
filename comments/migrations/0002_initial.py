# Generated by Django 5.2.1 on 2025-05-22 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('novels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='novels.novel'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comments.comment'),
        ),
    ]
