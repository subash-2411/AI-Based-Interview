from django.db.models.signals import post_save
from django.dispatch import receiver
from interview.models import InterviewSession
from .models import UserHistory

@receiver(post_save, sender=InterviewSession)
def update_user_history(sender, instance, created, **kwargs):
    if instance.is_completed:
        history, created = UserHistory.objects.get_or_create(user=instance.user)
        
        sessions = InterviewSession.objects.filter(user=instance.user, is_completed=True)
        history.total_interviews = sessions.count()
        
        total_score = sum([s.score for s in sessions])
        history.avg_score = total_score / history.total_interviews if history.total_interviews > 0 else 0
        
        # Gamification: 100 XP per interview + score percentage
        history.xp += 100 + int(instance.score)
        history.level = (history.xp // 1000) + 1
        
        history.save()
