# Generated by Django 2.2.7 on 2019-11-17 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='your_mail@gmail.com', max_length=254),
            preserve_default=False,
        ),
    ]
