import re
import requests
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from .models import Category, Product, Color, Size, Order, OrderItem, ContactMessage, HeroBanner, SiteSettings, TikTokReel
from .admin_views import smart_add_product
from django.core.management import call_command
from django.contrib import messages


def _fetch_tiktok_oembed(video_url):
    """Call TikTok oEmbed API (free, no auth) to get thumbnail + title."""
    try:
        resp = requests.get(
            'https://www.tiktok.com/oembed',
            params={'url': video_url},
            timeout=12,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                )
            }
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                'thumbnail_url': data.get('thumbnail_url', ''),
                'title': (data.get('title') or '')[:255],
            }
    except Exception:
        pass
    return None

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
    list_display = ['name', 'category', 'price', 'wholesale_price', 'badge']
    list_filter = ['category', 'badge']
    search_fields = ['name', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'article_no', 'volume_no', 'badge', 'description', 'image')
        }),
        ('Pricing', {
            'fields': ('price', 'old_price', 'discount_percent', 'wholesale_price', 'wholesale_package_size'),
            'description': 'Retail Price = regular selling price. Old Price = crossed-out original price. Wholesale Price = bulk order price.'
        }),
        ('Inventory & Links', {
            'fields': ('stock', 'link')
        }),
        ('Variants', {
            'fields': ('available_colors', 'available_sizes')
        }),
    )

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
        ('Social Media & TikTok Feed', {
            'fields': ('facebook_url', 'instagram_url', 'tiktok_profile_url', 'tiktok_sync_active', 'tiktok_embed_code'),
            'description': 'Paste your TikTok feed embed code (Elfsight, EmbedSocial, etc.) in the field below — it will appear automatically on the homepage.'
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

def _download_image(url):
    """Download image from URL, return ContentFile or None."""
    try:
        from django.core.files.base import ContentFile
        resp = requests.get(url, timeout=20, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if resp.status_code == 200 and resp.content:
            return ContentFile(resp.content)
    except Exception:
        pass
    return None


@admin.register(TikTokReel)
class TikTokReelAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_preview', 'title', 'is_active', 'created_at']
    list_editable = ['is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'video_id']
    exclude = ['video_id']
    change_list_template = 'admin/tiktokreel_change_list.html'

    def thumbnail_preview(self, obj):
        from django.utils.html import format_html
        # Prefer locally stored image
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;object-fit:cover;" />',
                obj.cover_image.url
            )
        if obj.cover_image_url:
            return format_html(
                '<img src="{}" style="height:60px;border-radius:6px;object-fit:cover;" />',
                obj.cover_image_url
            )
        return '—'
    thumbnail_preview.short_description = 'Preview'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('bulk-import/', self.admin_site.admin_view(self._bulk_import_view), name='tiktok-bulk-import'),
            path('refresh-thumbs/', self.admin_site.admin_view(self._refresh_thumbs_view), name='tiktok-refresh-thumbs'),
        ]
        return custom + urls

    def _bulk_import_view(self, request):
        """Admin pastes TikTok video URLs — system fetches thumbnails & saves locally."""
        results = []
        if request.method == 'POST':
            raw = request.POST.get('urls', '')
            urls = [u.strip() for u in raw.splitlines() if u.strip()]
            for video_url in urls:
                match = re.search(r'/video/(\d+)', video_url)
                if not match:
                    results.append({'url': video_url, 'status': 'error', 'msg': 'Not a valid TikTok video URL'})
                    continue
                video_id = match.group(1)
                username_match = re.search(r'@([a-zA-Z0-9._-]+)', video_url)
                username = username_match.group(1) if username_match else 'unknown'

                oembed = _fetch_tiktok_oembed(video_url)
                thumb_url = oembed['thumbnail_url'] if oembed else ''
                title = oembed['title'] if oembed else ''

                reel, created = TikTokReel.objects.get_or_create(
                    video_id=video_id,
                    defaults={'video_url': video_url, 'cover_image_url': thumb_url, 'title': title, 'is_active': True}
                )
                if not created:
                    reel.video_url = video_url
                    reel.cover_image_url = thumb_url or reel.cover_image_url
                    if title:
                        reel.title = title

                # Download thumbnail locally
                if thumb_url:
                    img_data = _download_image(thumb_url)
                    if img_data:
                        reel.cover_image.save(f'{video_id}.jpg', img_data, save=False)
                        results.append({'url': video_url, 'status': 'ok', 'msg': f'Saved — {title[:60] or video_id}'})
                    else:
                        results.append({'url': video_url, 'status': 'warn', 'msg': f'Saved URL only (image download failed) — {title[:50]}'})
                else:
                    results.append({'url': video_url, 'status': 'warn', 'msg': 'Saved without thumbnail (oEmbed failed)'})

                reel.save()

        return render(request, 'admin/tiktok_bulk_import.html', {
            'title': 'Bulk Import TikTok Videos',
            'results': results,
            'opts': TikTokReel._meta,
        })

    def _refresh_thumbs_view(self, request):
        """Re-fetch & re-download thumbnails for all active reels."""
        reels = TikTokReel.objects.filter(is_active=True)
        ok, fail = 0, 0
        for reel in reels:
            oembed = _fetch_tiktok_oembed(reel.video_url)
            if oembed and oembed['thumbnail_url']:
                img_data = _download_image(oembed['thumbnail_url'])
                if img_data:
                    reel.cover_image.save(f'{reel.video_id}.jpg', img_data, save=False)
                reel.cover_image_url = oembed['thumbnail_url']
                if not reel.title and oembed['title']:
                    reel.title = oembed['title']
                reel.save()
                ok += 1
            else:
                fail += 1
        if ok:
            messages.success(request, f'Refreshed {ok} thumbnail(s) successfully.')
        if fail:
            messages.warning(request, f'{fail} reel(s) failed — TikTok oEmbed may have rate-limited the request.')
        return redirect('../')

    def save_model(self, request, obj, form, change):
        if obj.video_url and not obj.video_id:
            match = re.search(r'/video/(\d+)', obj.video_url)
            obj.video_id = match.group(1) if match else str(abs(hash(obj.video_url)))[:18]

        if obj.video_url and not obj.cover_image and not obj.cover_image_url:
            oembed = _fetch_tiktok_oembed(obj.video_url)
            if oembed and oembed['thumbnail_url']:
                img_data = _download_image(oembed['thumbnail_url'])
                if img_data:
                    # save=False so we can call super().save_model() once
                    obj.cover_image.save(f'{obj.video_id}.jpg', img_data, save=False)
                obj.cover_image_url = oembed['thumbnail_url']
                if not obj.title and oembed['title']:
                    obj.title = oembed['title']
                messages.success(request, 'Thumbnail fetched and saved locally from TikTok.')
            else:
                messages.warning(request, 'oEmbed failed — add cover_image_url manually.')

        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ContactMessage)
