from django.db import models

from user.models import User


class Public(models.Model):
    images_public = models.ImageField(
        upload_to="publications_images",
        null=True, blank=True,
    )
    created = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="public",
        null=True,
        blank=True,
    )
    informations = models.TextField(blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')


class FavoritePublic(models.Model):
    public = models.ForeignKey(
        "publication.Public",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    publications = models.ForeignKey(
        Public, 
        on_delete=models.CASCADE, 
        verbose_name='Публикация', 
        blank=True, null=True, 
        related_name="comment_public",
    )

    author_comment = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор комментария', 
        blank=True, null=True, 
    )

    create_date_comment = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')