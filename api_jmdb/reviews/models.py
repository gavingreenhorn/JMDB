from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(db_index=True)
    year = models.IntegerField(validators=[validate_year])
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для отзывов."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(help_text='Leave your review here')
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Cannot give a score less than 1!'),
            MaxValueValidator(
                10, 'Cannot give a score higher than 10!')
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='publication date',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'),
        ]

    def __str__(self):
        return f'{self.title} review, score: {self.score}'


class Comment(models.Model):
    """Модель для комментариев."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(help_text='Leave your comment here')
    pub_date = models.DateTimeField(
        verbose_name='publication date',
        auto_now_add=True
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return f'Comment to review {self.review}'
