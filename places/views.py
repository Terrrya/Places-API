from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    extend_schema_view,
)
from rest_framework import viewsets

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


@extend_schema_view(
    list=extend_schema(description="Returns list of all places"),
    retrieve=extend_schema(
        description="Returns place detail information by id"
    ),
    update=extend_schema(
        description="Updates all information about place by id"
    ),
    partial_update=extend_schema(
        description="Updates partial information about place by id"
    ),
    create=extend_schema(description="Creates place"),
    destroy=extend_schema(description="Deletes place by id"),
)
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
            nearest_place_names = [queryset.first().name]
            for place in queryset.all():
                if point.distance(place.geom) < min_distance:
                    min_distance = point.distance(place.geom)
                    nearest_place_names = [place.name]
                elif point.distance(place.geom) == min_distance:
                    nearest_place_names.append(place.name)
            return queryset.filter(name__in=nearest_place_names)

        return queryset.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "coordinates",
                type=OpenApiTypes.STR,
                description="Search nearest places by coordinates "
                "(ex. ?coordinates=12.34343434,23.1223343)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
