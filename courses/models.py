from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from core.models import User

class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:  # Когда объект только создается, у него еще нет id
            self.created = timezone.now()  # проставляем дату создания
        self.updated = timezone.now()  # проставляем дату обновления
        return super().save(*args, **kwargs)


class Product(DatesModelMixin):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)  # Добавляем поле для мягкого удаления

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

class ProductAccess(DatesModelMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Доступ к продукту"
        verbose_name_plural = "Доступы к продуктам"
        unique_together = [['product', 'user']]  # Уникальность комбинации продукта и пользователя



class Lesson(DatesModelMixin):
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration = models.PositiveIntegerField()  # длительность в секундах

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['title']


class ProductLesson(DatesModelMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Урок продукта"
        verbose_name_plural = "Уроки продукта"


class LessonView(DatesModelMixin):
    VIEWED = 'viewed'
    NOT_VIEWED = 'not_viewed'
    STATUS_CHOICES = [
        (VIEWED, 'Просмотрено'),
        (NOT_VIEWED, 'Не просмотрено'),
    ]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    view_duration = models.PositiveIntegerField()  # длительность просмотра в секундах

    class Meta:
        verbose_name = "Просмотр урока"
        verbose_name_plural = "Просмотры уроков"
        unique_together = [['lesson', 'user']]

    @property
    def status(self):
        if self.view_duration >= self.lesson.duration * 0.8:
            return self.VIEWED
        return self.NOT_VIEWED

    def save(self, *args, **kwargs):
        if self.view_duration > self.lesson.duration:
            raise ValidationError("Продолжительность просмотра не может быть больше продолжительности урока.")
        super().save(*args, **kwargs)





