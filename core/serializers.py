from rest_framework import serializers
from .models import Category, Product, Color, Size, Order, OrderItem, ContactMessage, HeroBanner, SiteSettings, TikTokReel

class TikTokReelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TikTokReel
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image:
            return None
        image_url = str(obj.image)
        if image_url.startswith('http'):
            return image_url
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    available_colors = ColorSerializer(many=True, read_only=True)
    available_sizes = SizeSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        if not obj.image:
            return None
        image_url = str(obj.image)
        if image_url.startswith('http'):
            return image_url
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_items = serializers.JSONField(write_only=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'email', 'address', 'total_amount', 'created_at', 'status', 'items', 'order_items']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items', [])
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product_id = item_data.pop('product')
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, **item_data)
        return order

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class HeroBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    left_image = serializers.SerializerMethodField()
    right_image = serializers.SerializerMethodField()

    class Meta:
        model = HeroBanner
        fields = '__all__'

    def _get_image_url(self, image_field):
        if not image_field:
            return None
        image_url = str(image_field)
        if image_url.startswith('http'):
            return image_url
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(image_field.url)
        return image_field.url

    def get_image(self, obj):
        return self._get_image_url(obj.image)

    def get_left_image(self, obj):
        return self._get_image_url(obj.left_image)

    def get_right_image(self, obj):
        return self._get_image_url(obj.right_image)

class SiteSettingsSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    favicon = serializers.SerializerMethodField()

    class Meta:
        model = SiteSettings
        fields = '__all__'

    def _get_image_url(self, image_field):
        if not image_field:
            return None
        image_url = str(image_field)
        if image_url.startswith('http'):
            return image_url
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(image_field.url)
        return image_field.url

    def get_logo(self, obj):
        return self._get_image_url(obj.logo)

    def get_favicon(self, obj):
        return self._get_image_url(obj.favicon)
