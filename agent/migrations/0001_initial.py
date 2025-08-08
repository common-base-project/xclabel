from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('llm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=50)),
                ('config', models.JSONField(blank=True, default=dict)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='llm.llmprovider')),
            ],
            options={'db_table': 'xc_agent'},
        ),
        migrations.CreateModel(
            name='AgentSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100, unique=True)),
                ('messages', models.JSONField(blank=True, default=list)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='agent.agent')),
            ],
            options={'db_table': 'xc_agent_session'},
        ),
        migrations.CreateModel(
            name='WorkflowSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=100, unique=True)),
                ('nodes', models.JSONField(blank=True, default=list)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflows', to='agent.agent')),
            ],
            options={'db_table': 'xc_agent_workflow'},
        ),
    ]
