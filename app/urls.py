from rest_framework.routers import DefaultRouter

from app import views


router = DefaultRouter()
router.register(r'workflow', views.WorkflowViewSet, basename="workflow")
router.register(r'asset', views.AssetsViewset, basename="asset")
router.register(r'owner', views.OwnerViewset, basename="owner")
router.register(r'inventor', views.InventorViewset, basename="inventor")
router.register(r'technology', views.TechnologyViewset, basename="technology")
router.register(r'status', views.StatusViewset, basename="status")

urlpatterns = router.urls
