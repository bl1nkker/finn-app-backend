# Generated by Django 3.1.7 on 2021-07-23 13:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_signal'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Deduction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_deduction', models.CharField(choices=[('1', 'Аванс'), ('2', 'ЗП Безнал'), ('3', 'Мед Кн'), ('4', 'VR'), ('5', 'Бой'), ('6', 'Форма'), ('7', 'Удержание по сверкам'), ('8', 'Удержание по акту списания'), ('9', 'Штраф')], default='1', max_length=255)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.IntegerField(default=0)),
                ('commentary', models.TextField(default='', max_length=10000)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employee')),
            ],
        ),
    ]
