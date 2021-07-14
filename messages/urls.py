from .views import MessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='messages')
urlpatterns = router.urls
