from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from .models import Category, Product, Color, Size, Order, OrderItem, ContactMessage, HeroBanner, SiteSettings, TikTokReel
from .admin_views import smart_add_product
from django.core.management import call_command
from django.contrib import messages

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total_amount', 'created_at', 'status']
    list_editable = ['status']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'email', 'address']
    inlines = [OrderItemInline]
    actions = ['mark_as_delivered', 'mark_as_cancelled', 'mark_as_pending']

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
        self.message_user(request, "Selected orders marked as Delivered.")
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
        self.message_user(request, "Selected orders marked as Cancelled.")
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')
        self.message_user(request, "Selected orders marked as Pending.")
    mark_as_pending.short_description = "Mark selected orders as Pending"

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

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'banner_type', 'is_active']
    list_editable = ['is_active']

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'contact_email', 'contact_phone', 'tiktok_profile_url', 'tiktok_sync_active']
    fieldsets = (
        ('General Information', {
            'fields': ('brand_name', 'logo', 'favicon', 'address')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'whatsapp_number')
        }),
        ('Social Media & TikTok Sync', {
            'fields': ('facebook_url', 'instagram_url', 'tiktok_profile_url', 'tiktok_sync_active'),
            'description': 'Sync your TikTok reels by entering your profile URL and enabling sync.'
        }),
        ('Announcements', {
            'fields': ('announcement_text', 'show_announcement')
        }),
        ('Tax & Shipping', {
            'fields': ('shipping_fee', 'free_shipping_threshold', 'tax_percent')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.tiktok_sync_active and obj.tiktok_profile_url:
            try:
                call_command('fetch_reels')
                messages.success(request, f"TikTok Sync triggered for {obj.tiktok_profile_url}")
            except Exception as e:
                messages.error(request, f"Failed to sync TikTok reels: {str(e)}")

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
