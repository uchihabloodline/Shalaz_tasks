# Generated by Django 2.2.5 on 2019-09-29 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20190929_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='restaurent',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='API.Restaurent', to_field='res_id'),
            preserve_default=False,
        ),
    ]
