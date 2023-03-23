# Generated by Django 4.1.7 on 2023-03-17 16:58

from django.conf import settings
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
            name='Pet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='pets/')),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('medical_records', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.ImageField(upload_to='qrcodes/')),
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='petApp.pet')),
            ],
        ),
        migrations.CreateModel(
            name='PetProfileVisibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('visible', models.BooleanField(default=False)),
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='petApp.pet')),
            ],
        ),
    ]
