from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса", help_text='Укажите название курса')
    preview = models.ImageField(upload_to='materials/preview', blank=True, null=True, verbose_name='Превью курса', help_text='Загрузите превью')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса', help_text='Укажите описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название урока", help_text='Укажите название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание урока',
                                   help_text='Укажите описание урока')
    preview = models.ImageField(upload_to='materials/preview', blank=True, null=True, verbose_name='Превью курса',
                                help_text='Загрузите превью')
    link_to_video = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка на видео', help_text='Укажите ссылку на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name='lessons',)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
