from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Название категории"), max_length=200, db_index=True),
        slug = models.SlugField(_("Слаг"), max_length=200, unique=True)
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # Optimized: Add database indexes for better performance
        indexes = [
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("Название товара"), max_length=200, db_index=True),
        slug = models.SlugField(_("Слаг"), max_length=200, db_index=True),
        description = models.TextField(_("Описание"), blank=True)
    )

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE,
                                 verbose_name=_("Категория"))
    image = models.ImageField(_("Изображение"), upload_to='products/%Y/%m/%d', blank=True)
    # Optimized: Reduce thumbnail quality and size for better performance
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(300, 250)],  # Optimized size
                                      format='WEBP',  # Use WebP for better compression
                                      options={'quality': 85})  # Optimized quality

    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_("Запас (шт.)"), default=0)
    available = models.BooleanField(_("В наличии"), default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        # Optimized: Add database indexes for better query performance
        indexes = [
            models.Index(fields=['available', 'created']),
            models.Index(fields=['category', 'available']),
            models.Index(fields=['price']),
            models.Index(fields=['created']),
        ]
        # Optimized: Add ordering for consistent results
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])