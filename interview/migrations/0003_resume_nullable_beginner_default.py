from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_interviewsession_video_recording'),
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interviewsession',
            name='resume',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='resume.resume'
            ),
        ),
        migrations.AlterField(
            model_name='interviewsession',
            name='difficulty',
            field=models.CharField(default='Beginner', max_length=20),
        ),
    ]
