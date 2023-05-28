from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    geom = models.PointField()

    def __str__(self) -> str:
        return self.name
