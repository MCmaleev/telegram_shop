from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 related_name='products',
                                 verbose_name='Категория товара'
                                 )

    title = models.CharField(
        max_length=32,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=32,
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )
    picture = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Иконка')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title
