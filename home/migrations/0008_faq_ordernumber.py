# Generated by Django 3.0.4 on 2020-05-13 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200513_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='ordernumber',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
