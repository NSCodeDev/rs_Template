import re
import uuid

from django.db import models
from django.utils import timezone
from middlewares.tenantaware import get_current_tenant_id


class TimeStampedModel(models.Model):
    """Abstract base model with timestamp fields"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True, db_index=True)

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

    def delete(self, using=None, keep_parents=False, hard_delete=False):
        if hard_delete:
            return super().delete(using=using, keep_parents=keep_parents)
        else:
            from middlewares.tenantaware import get_current_user

            self.is_deleted = True
            self.deleted_at = timezone.now()

            # Set deleted_by from current user
            current_user = get_current_user()
            if current_user and current_user.get("user_id"):
                self.deleted_by = uuid.UUID(current_user.get("user_id"))

            self.save()
            return (1, {"SoftDeleteModel": 1})

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

    def save(self, *args, **kwargs):
        """Override save to automatically track user actions"""
        from middlewares.tenantaware import get_current_user

        # Get current user from thread-local storage
        current_user = get_current_user()

        if current_user:
            user_id = current_user.get("user_id")

            # Set created_by on creation
            if self._state.adding and user_id:
                if not self.created_by:
                    self.created_by = uuid.UUID(user_id)

            # Always update modified_by
            if user_id:
                self.modified_by = uuid.UUID(user_id)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"BaseModel {self.id}"


# Tenant aware model
class TenantModel(BaseModel):
    """Tenant aware model"""

    tenant_id = models.UUIDField(
        null=True, blank=True, db_index=True, help_text="Tenant identifier"
    )

    class Meta(BaseModel.Meta):
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


# Tenant-aware manager mixin
class TenantAwareManager(models.Manager):
    """Abstract base model for tenant-aware models"""

    def get_queryset(self):
        tenant_id = get_current_tenant_id()
        qs = super().get_queryset()
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        return qs
