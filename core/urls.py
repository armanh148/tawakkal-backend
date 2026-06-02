from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet, ColorViewSet, 
    SizeViewSet, OrderViewSet, ContactMessageViewSet, HeroBannerViewSet,
    SiteSettingsViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'messages', ContactMessageViewSet)
router.register(r'hero-banners', HeroBannerViewSet)
router.register(r'site-settings', SiteSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
