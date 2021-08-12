# Generated by Django 3.1.7 on 2021-07-22 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210612_0729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_signal', models.CharField(choices=[('1', 'Отрицательный остаток'), ('2', 'Проверить документы'), ('3', 'Несоответствие наличных денег')], default='1', max_length=255)),
                ('message', models.TextField(default='', max_length=10000)),
                ('facility', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.facility')),
            ],
        ),
    ]
