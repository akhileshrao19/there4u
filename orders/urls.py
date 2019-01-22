from rest_framework import routers

from .views import OrderView

router = routers.DefaultRouter()
router.register(r'order', OrderView)
urlpatterns = router.urls