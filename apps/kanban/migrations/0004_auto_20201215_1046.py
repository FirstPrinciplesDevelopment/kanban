# Generated by Django 3.1.3 on 2020-12-15 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0003_auto_20201212_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='members',
        ),
        migrations.AlterField(
            model_name='attachment',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='kanban.board'),
        ),
        migrations.AlterField(
            model_name='label',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labels', to='kanban.board'),
        ),
        migrations.AlterField(
            model_name='member',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='kanban.board'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tag',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to=settings.AUTH_USER_MODEL),
        ),
    ]