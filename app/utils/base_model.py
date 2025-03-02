from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    enabled = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    user_created = models.ForeignKey(
        User,
        related_name="%(class)ss_created",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    user_modified = models.ForeignKey(
        User,
        related_name="%(class)ss_modified",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    user_deleted = models.ForeignKey(
        User,
        related_name="%(class)ss_deleted",
        null=True,
        blank=True,
        default=None,
        on_delete=models.PROTECT,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def soft_delete(self, user: User = None):
        self.deleted = True
        if user:
            self.user_deleted = user
        self.save(update_fields=["deleted", "user_deleted"])

    def restore(self):
        self.deleted = False
        self.save(update_fields=["deleted"])

    def hard_delete(self):
        super().delete()
