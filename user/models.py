from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ChoiceField
from django.db.models import QuerySet

    

class CustomUserQuerySet(QuerySet):
    def followed_by_user(self, user_id):
        follow_object = Follow.objects.filter(follower_id=user_id).values_list("following_id", flat=True)
        return self.filter(id__in=follow_object)

    def follows_user(self, user_id):
        follow_object = Follow.objects.filter(following_id=user_id).values_list("follower_id", flat=True)
        return self.filter(id__in=follow_object)


class User(AbstractUser):
    following: QuerySet["Follow"]
    followers: QuerySet["Follow"]
    objects = UserManager.from_queryset(CustomUserQuerySet)()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status_profile = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(
        upload_to="category_images",
        null=True, blank=True,
    )


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (
            'following', 
            'follower',
        )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()