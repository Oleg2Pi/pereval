from django.db import models
from .service import get_level_list, get_status_list, get_new_status


class PerevalModel(models.Model):
    """Перевал"""

    beauty_title = models.CharField(max_length=255, verbose_name='Индекс', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    other_title = models.CharField(max_length=255, verbose_name='Другое название', null=True, blank=True)
    connect = models.TextField(null=True, blank=True, verbose_name='Соединяет')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='Пользователь')
    coord = models.OneToOneField('PerevalCoordinate', on_delete=models.CASCADE, verbose_name='Координаты')
    level = models.ForeignKey('PerevalLevel', on_delete=models.CASCADE, verbose_name='Уровень')
    status = models.CharField(max_length=8, choices=get_status_list(), default=get_new_status(), verbose_name='Статус')

    def __str__(self):
        return f'{self.beauty_title}, {self.title}'
    

class UserModel(models.Model):
    """Пользователь"""

    surname = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    otc = models.CharField(max_length=255, verbose_name='Отчество')
    email = models.EmailField(verbose_name='Почта')
    phone = models.CharField(max_length=11, verbose_name='Телефон')

    def __str__(self):
        return f'{self.surname} {self.name}'


class PerevalCoordinate(models.Model):
    """Координаты"""

    latitude = models.FloatField(max_length=30, verbose_name='Широта', null=True, blank=True)
    longitude = models.FloatField(max_length=30, verbose_name='Долгота', null=True, blank=True)
    height = models.FloatField(max_length=20, verbose_name='Высота', null=True, blank=True)

    def __str__(self):
        return f'широта:{self.latitude}, долгота:{self.longitude}, высота:{self.height}'
    

class PerevalLevel(models.Model):
    """Категория трудности"""

    winter = models.CharField(max_length=2, choices=get_level_list(), verbose_name='Зима', null=True, blank=True)
    summer = models.CharField(max_length=2, choices=get_level_list(), verbose_name='Лето', null=True, blank=True)
    autumn = models.CharField(max_length=2, choices=get_level_list(), verbose_name='Осень', null=True, blank=True)
    spring = models.CharField(max_length=2, choices=get_level_list(), verbose_name='Весна', null=True, blank=True)

    def __str__(self):
        l_winter = f'Зима - {self.winter};' if self.winter else ""
        l_summer = f'Лето - {self.summer};' if self.summer else ""
        l_autumn = f'Осень - {self.autumn};' if self.autumn else ""
        l_spring = f'Весна - {self.spring};' if self.spring else ""

        return f'{l_winter} {l_summer} {l_autumn} {l_spring}'
    

class ImageModel(models.Model):
    """Изображение перевалов"""

    title = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    data = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Изображение', null=True, blank=True)
    pereval = models.ForeignKey(PerevalModel, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'