from django.contrib.gis.geos import Point
from django.db.models import Q
from django.shortcuts import reverse
from django.test import TestCase, Client
from rest_framework import status

from places.models import Place
from places.serializers import PlaceSerializer

PLACE_URL = reverse("places:place-list")


def sample_place(**params) -> Place:
    default = {
        "name": "test place",
        "description": "test description",
        "geom": Point((0, 0)),
    }
    default.update(params)
    return Place.objects.create(**default)


def detail_place_url(place_id: int) -> str:
    return reverse("places:place-detail", kwargs={"pk": place_id})


class PlacesApiTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.place = sample_place()

    def test_list_places(self) -> None:
        sample_place(name="test places 2")
        sample_place(name="test places 3")
        places = Place.objects.all()

        response = self.client.get(PLACE_URL)
        serializer = PlaceSerializer(places, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_place(self) -> None:
        response = self.client.get(detail_place_url(self.place.id))
        serializer = PlaceSerializer(self.place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_place(self) -> None:
        payload = {
            "name": "payload place",
            "description": "payload description",
            "geom": {"type": "Point", "coordinates": [1, 1]},
        }

        response = self.client.post(
            path=PLACE_URL, data=payload, content_type="application/json"
        )
        place = Place.objects.get(name=response.data["name"])

        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_place(self) -> None:
        payload = {
            "name": "new place",
            "description": "new description",
            "geom": {"type": "Point", "coordinates": [2, 2]},
        }

        response = self.client.put(
            path=detail_place_url(self.place.id),
            data=payload,
            content_type="application/json",
        )
        place = Place.objects.get(name=response.data["name"])

        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_partial_update_place(self) -> None:
        payload = {
            "geom": {"type": "Point", "coordinates": [2, 2]},
        }

        response = self.client.patch(
            path=detail_place_url(self.place.id),
            data=payload,
            content_type="application/json",
        )
        place = Place.objects.get(name=response.data["name"])

        serializer = PlaceSerializer(place)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_place(self) -> None:
        response = self.client.delete(
            path=detail_place_url(self.place.id),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_places_returns_place_nearest_to_params_coordinates(
        self,
    ) -> None:
        place2 = sample_place(name="test place 2", geom=Point((1, 1)))
        place3 = sample_place(name="test place 3", geom=Point((2, 2)))

        response = self.client.get(PLACE_URL + "?coordinates=1.1,1.1")

        serializer = PlaceSerializer(place2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0], serializer.data)

    def test_list_places_returns_all_nearest_places_to_params_coordinates(
        self,
    ) -> None:
        place2 = sample_place(name="test place 2", geom=Point((1, 1)))
        place3 = sample_place(name="test place 3", geom=Point((1, 1)))

        response = self.client.get(PLACE_URL + "?coordinates=1.1,1.1")
        nearest_places = Place.objects.filter(
            Q(name="test place 2") | Q(name="test place 3")
        )

        serializer = PlaceSerializer(nearest_places, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
