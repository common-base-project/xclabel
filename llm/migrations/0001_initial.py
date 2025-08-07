# Generated manually as Django is unavailable
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='LLMProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('base_url', models.CharField(max_length=255)),
                ('api_key', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('extra', models.JSONField(blank=True, null=True)),
            ],
            options={
                'db_table': 'xc_llm_provider',
            },
        ),
    ]
