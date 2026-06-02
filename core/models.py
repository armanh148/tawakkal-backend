from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    volume_no = models.CharField(max_length=100, null=True, blank=True)
    article_no = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.CharField(max_length=50) # New Price
    old_price = models.CharField(max_length=50, null=True, blank=True)
    discount_percent = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)
    badge = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    available_colors = models.ManyToManyField(Color, blank=True)
    available_sizes = models.ManyToManyField(Size, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.article_no:
            last_product = Product.objects.order_by('id').last()
            if last_product:
                last_id = last_product.id
                self.article_no = f"TW-{(last_id + 1):04d}"
            else:
                self.article_no = "TW-0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', null=True, blank=True)

    def __str__(self):
        return f"Gallery for {self.product.name}"

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    total_amount = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"

class HeroBanner(models.Model):
    BANNER_TYPES = (
        ('MAIN', 'Main Hero'),
        ('NEW_ARRIVAL', 'New Arrival Section'),
        ('BEST_SELLER', 'Best Seller Section'),
    )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    left_image = models.ImageField(upload_to='banners/', null=True, blank=True)
    right_image = models.ImageField(upload_to='banners/', null=True, blank=True)
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='MAIN')
    button_text = models.CharField(max_length=50, default="Shop Now")
    link = models.CharField(max_length=255, default="/products")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.banner_type}] {self.title}"

class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=255, default="Tawakkal")
    logo = models.ImageField(upload_to='settings/', null=True, blank=True)
    favicon = models.ImageField(upload_to='settings/', null=True, blank=True)
    contact_email = models.EmailField(default="info@tawakkal.com")
    contact_phone = models.CharField(max_length=20, default="+92 300 1234567")
    address = models.TextField(default="Karachi, Pakistan")
    
    # Social Links
    facebook_url = models.URLField(max_length=500, blank=True, null=True)
    instagram_url = models.URLField(max_length=500, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Operational
    shipping_fee = models.IntegerField(default=250)
    free_shipping_threshold = models.IntegerField(default=5000)
    tax_percent = models.IntegerField(default=0)
    
    # Announcement Bar
    announcement_text = models.CharField(max_length=255, default="Free Shipping on orders above PKR 5,000")
    show_announcement = models.BooleanField(default=True)

    def __str__(self):
        return "Global Site Settings"
    
    class Meta:
        verbose_name_plural = "Site Settings"
