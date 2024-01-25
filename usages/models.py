from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class UsageType(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    factor = models.FloatField(validators=[MinValueValidator(0)])

    class Meta:
        managed = True
        db_table = "usage_types"
        unique_together = ('name', 'unit')

    def __str__(self):
        return f'{self.name} - {self.unit}'


class Usage(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='usages'
    )
    usage_type = models.ForeignKey(
        UsageType,
        on_delete=models.DO_NOTHING,
        related_name='usages'
    )
    calculated_emissions = models.FloatField(
        validators=[MinValueValidator(0)],
        default=0
    )
    amount = models.FloatField(validators=[MinValueValidator(0)])
    usage_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = "usage"

    def __str__(self):
        return f'{self.user.name} - {self.usage_type.name}'
