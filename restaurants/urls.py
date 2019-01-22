from rest_framework import routers

from .views import RestaurantView

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantView)
urlpatterns = router.urls