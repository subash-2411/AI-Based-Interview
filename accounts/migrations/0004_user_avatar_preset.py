from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_themepreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar_preset',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
