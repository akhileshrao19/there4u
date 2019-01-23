from rest_framework import routers

from .views import RestaurantView, MenuView

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantView)
router.register(r'menu', MenuView)
urlpatterns = router.urls
