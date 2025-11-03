import re
import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class UserTrackingModel(models.Model):
    """Abstract base model for user tracking"""

    created_by = models.UUIDField(
        null=True, blank=True, db_index=True
    )  # Store user UUID from  request context
    modified_by = models.UUIDField(
        null=True, blank=True
    )  # Store user UUID from  request context

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Abstract base model for soft delete"""

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.UUIDField(
        null=True, blank=True
    )  # Store user UUID from  request context

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, hard_delete=False):  # type: ignore
        if hard_delete:
            super().delete(using=using, keep_parents=keep_parents)
        else:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()
        return self

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()


class ActiveStatusModel(models.Model):
    """Abstract base model for active/inactive status"""

    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base model with UUID primary key"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(  # type: ignore
    TimeStampedModel, UserTrackingModel, SoftDeleteModel, ActiveStatusModel
):
    """Complete base model for microservices"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(
        TimeStampedModel.Meta,
        UserTrackingModel.Meta,
        SoftDeleteModel.Meta,
        ActiveStatusModel.Meta,
    ):
        abstract = True


# Custom manager to handle soft-deleted objects


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted objects"""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        return super().get_queryset()

    def deleted_only(self):
        return super().get_queryset().filter(is_deleted=True)

    def active_only(self):
        return self.get_queryset().filter(is_active=True)
