# Generated by Django 3.0.4 on 2020-05-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='answer',
            field=models.TextField(),
        ),
    ]