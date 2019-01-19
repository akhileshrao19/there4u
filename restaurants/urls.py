from rest_framework import routers

from .views import RestaurantView, DishView

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantView)
router.register(r'dish', DishView)
urlpatterns = router.urls