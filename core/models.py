from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class PetUser(AbstractUser):
    PET_TYPE_CHOICES = [
        ('dog', 'Собака'),
        ('cat', 'Кошка'),
        ('bird', 'Птица'),
        ('other', 'Другое')
    ]

    pet_type = models.CharField(
        max_length=50,
        choices=PET_TYPE_CHOICES,
        default='dog'
    )

    def get_pet_type_display(self):
        return dict(self.PET_TYPE_CHOICES).get(self.pet_type, self.pet_type)

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    bio = models.TextField(blank=True, max_length=500)
    pet_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    subscriptions = models.ManyToManyField(
        'self',
        through='Subscription',
        symmetrical=False,
        related_name='subscribers',
        verbose_name='Подписки'
    )


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        PetUser,
        on_delete=models.CASCADE,
        related_name='following'
    )
    target = models.ForeignKey(
        PetUser,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'target')
        ordering = ['-created_at']


class Post(models.Model):
    author = models.ForeignKey(PetUser, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(max_length=2000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.pet_name}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    def user_has_liked(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(PetUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(PetUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')