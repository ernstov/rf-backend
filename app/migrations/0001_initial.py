# Generated by Django 3.2.12 on 2022-03-29 20:12

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
                ('assignee_type', models.CharField(choices=[('fmcg', 'Large FMCG'), ('packaging compititor', 'Packaging Compititor'), ('sme', 'SME (Small/Medium) Enterprise'), ('pvt individual', 'Private Individual'), ('univeristy', 'University / TTO'), ('other', 'Other')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CPCCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Inventor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
                ('owner_type', models.CharField(choices=[('fmcg', 'Large FMCG'), ('packaging compititor', 'Packaging Compititor'), ('sme', 'SME (Small/Medium) Enterprise'), ('pvt individual', 'Private Individual'), ('univeristy', 'University / TTO'), ('other', 'Other')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='TechnologyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('project', 'Project'), ('program', 'Program')], max_length=50)),
                ('archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shortlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('archived', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('new', 'New'), ('ute', 'Under Technical Evaluation'), ('uce', 'Under Commercial Evaluation'), ('rejected', 'Rejected'), ('orphan', 'Orphan'), ('under negotiation', 'Under Negotiation'), ('acquired', 'Acquired'), ('unavailable', 'Unavailable')], max_length=50)),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.workflow')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('archived', models.BooleanField(default=False)),
                ('family_id', models.CharField(max_length=255, unique=True)),
                ('patent_numbers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None, unique=True)),
                ('description', models.TextField()),
                ('abstract', models.TextField()),
                ('claims', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('priority_date', models.DateField()),
                ('publication_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('cost_to_date', models.FloatField(blank=True, null=True)),
                ('future_cost_projection', models.FloatField(blank=True, null=True)),
                ('cipher_score', models.FloatField(blank=True, null=True)),
                ('pvix_score', models.FloatField(blank=True, null=True)),
                ('organisation', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, unique=True), blank=True, null=True, size=None)),
                ('backward_citations', models.IntegerField(blank=True, null=True)),
                ('forward_citations', models.IntegerField(blank=True, null=True)),
                ('prepatent', models.BooleanField(blank=True, null=True)),
                ('assigness', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, null=True, size=None)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cpc_code', models.ManyToManyField(blank=True, to='app.CPCCode')),
                ('expired_territories', models.ManyToManyField(blank=True, related_name='expired_territories', to='app.Country')),
                ('granted_territories', models.ManyToManyField(blank=True, related_name='granted_territories', to='app.Country')),
                ('inventors', models.ManyToManyField(blank=True, to='app.Inventor')),
                ('owners', models.ManyToManyField(to='app.Owner')),
                ('pending_territories', models.ManyToManyField(blank=True, related_name='pending_territories', to='app.Country')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.source')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.status')),
                ('technology_types', models.ManyToManyField(to='app.TechnologyType')),
                ('workflow', models.ManyToManyField(to='app.Workflow')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
