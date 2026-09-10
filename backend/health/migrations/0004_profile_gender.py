from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("health", "0003_eyedetection_causes_eyedetection_disease_info_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="gender",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
