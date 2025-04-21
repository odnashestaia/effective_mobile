from rest_framework.routers import DefaultRouter

from .views import AdViewSet, ExchangeProposalViewSet

router = DefaultRouter()
router.register(r"barter", AdViewSet, basename="barter")
router.register(r"proposals", ExchangeProposalViewSet, basename="proposals")

urlpatterns = router.urls
