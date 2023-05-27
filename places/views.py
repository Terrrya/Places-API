from django.db.models import QuerySet
from rest_framework import viewsets
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point

from places.models import Place
from places.serializers import PlaceSerializer


def params_to_point(string: str) -> Point:
    """
    Function get string with coordinates and transform it in Point
    """
    coordinates = list(map(float, tuple(string.split(","))))
    if len(coordinates) != 2:
        raise ValidationError({"coordinates": "coordinates incorrect"})
    return Point(coordinates)


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_queryset(self) -> QuerySet:
        """
        Search for the nearest places with coordinates from the parameters
        """
        queryset = Place.objects

        coordinates = self.request.query_params.get("coordinates")
        if coordinates:
            point = params_to_point(coordinates)
            min_distance = point.distance(queryset.first().geom)
            nearest_place_ids = [queryset.first().id]
            for place in queryset.all():
                if point.distance(place.geom) < min_distance:
                    min_distance = point.distance(place.geom)
                    nearest_place_ids = [place.id]
                elif point.distance(place.geom) == min_distance:
                    nearest_place_ids.append(place.id)
            return queryset.filter(id__in=nearest_place_ids)

        return queryset.all()
