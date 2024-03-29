# Generated by Django 4.2 on 2023-06-04 15:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import message.models.message_models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('message', models.TextField(blank=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='message.messages')),
                ('is_seen', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to=message.models.message_models.messages_file_path))
            ],
            bases=('core.uuid',),
        ),
    ]
