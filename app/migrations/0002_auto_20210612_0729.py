# Generated by Django 3.1.7 on 2021-06-12 07:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_delete_userrole'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('added_at', models.DateField(default=django.utils.timezone.now)),
                ('invoice_number', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('tax_amount', models.FloatField(default=0)),
                ('comment', models.TextField(default='', max_length=10000)),
                ('payment_type', models.CharField(default='cash', max_length=255)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('facility', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.facility')),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_scan', models.CharField(choices=[('1', 'Накладная'), ('2', 'Расходы'), ('3', 'Сканы'), ('4', 'Уставные Документы')], default='1', max_length=255)),
                ('added_at', models.DateField(auto_now_add=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('file', models.FileField(upload_to='')),
                ('facility', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.facility')),
            ],
        ),
        migrations.RemoveField(
            model_name='income',
            name='added_by',
        ),
        migrations.RemoveField(
            model_name='income',
            name='category',
        ),
        migrations.RemoveField(
            model_name='income',
            name='facility',
        ),
        migrations.AddField(
            model_name='importer',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userfacility',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.role'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='payment_type',
            field=models.CharField(choices=[('1', 'Оклад'), ('2', 'Почасовая ставка'), ('3', 'Посуточная ставка')], default='1', max_length=255),
        ),
        migrations.AlterField(
            model_name='employee',
            name='profile_picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='subdivision',
            field=models.CharField(choices=[('1', 'Администрация'), ('2', 'Бар'), ('3', 'Официанты'), ('4', 'Кухня'), ('5', 'Технический Персонал')], default='1', max_length=255),
        ),
        migrations.AlterField(
            model_name='revenue',
            name='added_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='Expense',
        ),
        migrations.DeleteModel(
            name='ExpenseCategory',
        ),
        migrations.DeleteModel(
            name='Income',
        ),
        migrations.DeleteModel(
            name='IncomeCategory',
        ),
        migrations.AddField(
            model_name='invoice',
            name='importer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.importer'),
        ),
    ]
