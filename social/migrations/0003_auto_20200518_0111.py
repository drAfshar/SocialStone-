# Generated by Django 3.0.4 on 2020-05-17 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_reply_reply_to_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='social.Comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='social.Post')),
                ('reply', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='social.Reply')),
                ('view', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='social.View')),
            ],
        ),
    ]