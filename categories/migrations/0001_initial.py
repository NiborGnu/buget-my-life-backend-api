# Generated by Django 5.1.1 on 2024-10-20 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55, unique=True)),
                ('category_type', models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], max_length=55)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='categories.category')),
            ],
            options={
                'unique_together': {('name', 'category_type')},
            },
        ),
    ]
