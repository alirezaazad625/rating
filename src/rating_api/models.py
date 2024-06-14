from enum import Enum

from django.db import models


class RatingStatus(Enum):
    PENDING = "PENDING",
    APPROVED = "APPROVED",

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value[0]) for i in cls)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField()
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    status = models.CharField(max_length=255, choices=RatingStatus.choices(), default=RatingStatus.APPROVED)

    class Meta:
        indexes = [
            models.Index(fields=['post_id']),
            models.Index(fields=['post_id', 'user_id'])
        ]


class PostRating(models.Model):
    id = models.AutoField(primary_key=True)
    count = models.BigIntegerField(default=0)
    sum = models.BigIntegerField(default=0)
    post_id = models.IntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=['post_id'])]
