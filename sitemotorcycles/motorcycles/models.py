from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Motorcycles.Status.PUBLISHED)


class Motorcycles(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'В очереди'
        PUBLISHED = 1, 'Опубликовано'

    brand = models.CharField(
        max_length=100,
        verbose_name='Марка мотоцикла',
    )

    bike_model = models.CharField(
        max_length=100,
        verbose_name='Модель мотоцикла',
    )

    photo = models.ImageField(
        upload_to="motorcyclesphoto/%Y/%m/%d/",
        default=None,
        verbose_name='Фото мотоцикла',
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=155,
        unique=True,
        db_index=True,
        verbose_name='Slug',
        validators=[
            MinLengthValidator(5, message="Минимум 5 символов"),
            MaxLengthValidator(100, message="Максимум 100 символов"),
        ],
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание модели',
    )

    kind = models.ForeignKey(
        'KindOfMotorcycle',
        on_delete=models.PROTECT,
        related_name='post',
        verbose_name='Класс мотоцикла'
    )

    type = models.ForeignKey(
        'EngineType',
        on_delete=models.PROTECT,
        related_name='types',
        verbose_name='Тип двигателя'
    )

    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус"
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Время изменения"
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.bike_model

    class Meta:
        verbose_name = "Мотоцикл"
        verbose_name_plural = "Мотоциклы"
        ordering = ['time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class KindOfMotorcycle(models.Model):
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Класс мотоцикла',
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )

    photo_kind = models.ImageField(
        upload_to="motorcyclesphoto/%Y/%m/%d/",
        default=None,
        verbose_name='Фото',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Класс мотоцикла"
        verbose_name_plural = "Классы мотоциклов"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('kind', kwargs={'kind_slug': self.slug})


class EngineType(models.Model):
    type = models.CharField(
        max_length=100,
        db_index=True
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )

    photo_engine = models.ImageField(
        upload_to="motorcyclesphoto/%Y/%m/%d/",
        default=None,
        verbose_name='Фото',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Тип двигателя"
        verbose_name_plural = "Типы двигателя"

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse('type', kwargs={'type_slug': self.slug})


class Favorite(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='fav_user',
        verbose_name='Пользователь'
    )

    motorcycles = models.ForeignKey(
        Motorcycles,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Мотоциклы',
    )

    class Meta:
        verbose_name = "Список избранного"
        verbose_name_plural = "Списки избранного"

    def __str__(self):
        return f'{self.user.username} | {self.motorcycles.slug}'


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    url = models.CharField(
        verbose_name='Ссылка',
        max_length=255
    )
    position = models.PositiveIntegerField(
        verbose_name='Позиция',
        default=1
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('position',)
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def get_absolute_url(self):
        return reverse(f'{self.url}')
