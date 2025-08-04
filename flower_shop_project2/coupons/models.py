from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Coupon(models.Model):
    code = models.CharField(_("Код"), max_length=50, unique=True)
    valid_from = models.DateTimeField(_("Действителен с"))
    valid_to = models.DateTimeField(_("Действителен до"))
    discount = models.IntegerField(
        _("Скидка (%)"),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(_("Активен"))

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code