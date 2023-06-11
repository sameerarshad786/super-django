# Generated by Django 4.2 on 2023-04-28 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models.comments_model
import posts.models.posts_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0002_comments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Remarks',
            fields=[
                ('uuid_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.uuid')),
                ('popularity', models.CharField(choices=[('like', 'LIKE'), ('heart', 'HEART'), ('funny', 'FUNNY'), ('insightful', 'INSIGHTFUL'), ('disappoint', 'DISAPPOINT')], max_length=11)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.comments')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('core.uuid',),
        ),
    ]