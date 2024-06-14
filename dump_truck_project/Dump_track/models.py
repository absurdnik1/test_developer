from django.db import models
from django.core.validators import (MinValueValidator,)
from django.contrib.gis.db import models as gismodels


class DumpTruck(models.Model):
    """Модель самосвала."""
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=50,
                            verbose_name='dump_track_name')
    lifting_capacity = models.PositiveIntegerField(
        verbose_name='грузоподъёмность',
        validators=[
            MinValueValidator(
                0,
                message='Значение грузоподъёмности не может быть отрицательным'
                )]
    )
    current_weight = models.PositiveIntegerField()
    SiO2 = models.PositiveIntegerField()
    FE = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Самосвал'
        verbose_name_plural = 'Самосвалы'
    
    def __str__(self):
        return f'{self.number} - {self.name}'


class Storage(models.Model):
    """Модель склада."""
    name = models.CharField(max_length=50,
                            verbose_name='Склад')
    current_weight = models.PositiveIntegerField()
    SiO2 = models.PositiveIntegerField()
    FE = models.PositiveIntegerField()
    polygon = gismodels.PolygonField(srid=4326)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
    
    def __str__(self):
        return f'На складе {self.current_weight} т. руды.'


class Location(models.Model):
    dump_truck = models.ForeignKey(DumpTruck, on_delete=models.CASCADE)
    location = gismodels.PointField(srid=4326)

    class Meta:
        verbose_name = 'Координаты выгрузки'
        verbose_name_plural = 'Координаты выгрузки'