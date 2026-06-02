from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from .models import Category, Product, Color, Size, Order, OrderItem, ContactMessage, HeroBanner, SiteSettings
from .admin_views import smart_add_product

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total_amount', 'created_at', 'is_delivered']
    inlines = [OrderItemInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'badge']
    list_filter = ['category', 'badge']
    search_fields = ['name', 'description']
    
    change_list_template = "admin/product_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('smart-add/', self.admin_site.admin_view(smart_add_product), name='smart-add-product'),
        ]
        return custom_urls + urls

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'contact_email', 'contact_phone']

    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect to the first instance's change page
        obj = self.model.objects.first()
        if obj:
            return redirect(reverse('admin:core_sitesettings_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ContactMessage)
