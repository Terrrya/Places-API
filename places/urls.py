from rest_framework import routers

from places.views import PlaceViewSet


router = routers.DefaultRouter()
router.register("places", PlaceViewSet)


urlpatterns = router.urls

app_name = "places"
