from rest_framework import viewsets, filters
from .models import Category, Product, Color, Size, Order, ContactMessage, HeroBanner, SiteSettings
from .serializers import (
    CategorySerializer, ProductSerializer, ColorSerializer, 
    SizeSerializer, OrderSerializer, ContactMessageSerializer, HeroBannerSerializer,
    SiteSettingsSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'badge']
    ordering_fields = ['created_at', 'price']

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category and category != 'All':
            queryset = queryset.filter(category__name=category)
        
        badge = self.request.query_params.get('badge')
        if badge:
            queryset = queryset.filter(badge=badge)
            
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

class HeroBannerViewSet(viewsets.ModelViewSet):
    queryset = HeroBanner.objects.all()
    serializer_class = HeroBannerSerializer

class SiteSettingsViewSet(viewsets.ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    def get_queryset(self):
        # Always return only the first one (global settings)
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create()
        return SiteSettings.objects.all()[:1]
