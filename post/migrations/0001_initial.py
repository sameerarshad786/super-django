# Generated by Django 4.0.4 on 2022-10-19 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.models.post_model
import post.models.postremark_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('text', models.TextField()),
                ('files', models.FileField(upload_to=post.models.post_model.post_uploaded_files, verbose_name='file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=('core.uuid',),
        ),
        migrations.CreateModel(
            name='PostRemark',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('popularity', models.CharField(choices=[('like', 'LIKE'), ('dislike', 'DISLIKE')], max_length=11)),
                ('on_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('core.uuid',),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('comment', models.TextField(blank=True)),
                ('files', models.FileField(blank=True, upload_to=post.models.postremark_model.comment_media_path, verbose_name='file')),
                ('on_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('core.uuid',),
        ),
    ]
