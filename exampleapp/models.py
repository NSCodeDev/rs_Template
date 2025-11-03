from django.db import models

from core.models.base import BaseModel, SoftDeleteManager

# Create your models here.


class ExampleModel(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    objects = SoftDeleteManager()  # Use custom manager

    class Meta(BaseModel.Meta):
        verbose_name = "Example Model"
        verbose_name_plural = "Example Models"
