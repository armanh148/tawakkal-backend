import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Category, Product, Color, Size

def populate_products():
    # 1. Get Categories
    unstitched = Category.objects.get(name='Unstitched')
    rtw = Category.objects.get(name='Ready to Wear')
    luxe = Category.objects.get(name='Luxe Edition')
    acc = Category.objects.get(name='Accessories')

    # 2. Get Colors
    colors = ['Red', 'Blue', 'Black', 'Emerald Green', 'Maroon', 'White', 'Gold', 'Pink', 'Purple', 'Teal']
    color_objs = {}
    for c in colors:
        obj, _ = Color.objects.get_or_create(name=c)
        color_objs[c] = obj

    # 3. Get Sizes
    sizes = ['XS', 'S', 'M', 'L', 'XL', 'Standard']
    size_objs = {}
    for s in sizes:
        obj, _ = Size.objects.get_or_create(name=s)
        size_objs[s] = obj

    # 4. Product Data (5 per category)
    data = [
        # --- UNSTITCHED ---
        {
            'name': 'Luxury Lawn 3-Piece Suite',
            'category': unstitched, 'price': '4,500', 'old_price': '6,000', 'discount_percent': 25, 'stock': 50,
            'badge': 'New', 'description': 'Premium quality 3-piece unstitched lawn suite.',
            'colors': ['Emerald Green', 'Maroon'], 'sizes': ['Standard'], 'image': 'products/unstitched-1.jpg'
        },
        {
            'name': 'Premium Swiss Voile 2-Piece',
            'category': unstitched, 'price': '3,800', 'old_price': '4,500', 'discount_percent': 15, 'stock': 40,
            'badge': 'Best Seller', 'description': 'Elegant 2-piece swiss voile suite for formal wear.',
            'colors': ['White', 'Pink'], 'sizes': ['Standard'], 'image': 'products/unstitched-1.jpg'
        },
        {
            'name': 'Printed Lawn Karandi',
            'category': unstitched, 'price': '2,900', 'old_price': '3,500', 'discount_percent': 17, 'stock': 60,
            'badge': 'Sale', 'description': 'Soft karandi fabric with vibrant digital prints.',
            'colors': ['Blue', 'Teal'], 'sizes': ['Standard'], 'image': 'products/unstitched-1.jpg'
        },
        {
            'name': 'Embroidered Cotton Satin',
            'category': unstitched, 'price': '5,200', 'old_price': '6,500', 'discount_percent': 20, 'stock': 30,
            'badge': 'Limited', 'description': 'Rich cotton satin with intricate thread work.',
            'colors': ['Black', 'Gold'], 'sizes': ['Standard'], 'image': 'products/unstitched-1.jpg'
        },
        {
            'name': 'Digital Printed Khaddar',
            'category': unstitched, 'price': '2,500', 'old_price': '3,200', 'discount_percent': 22, 'stock': 80,
            'badge': 'New', 'description': 'Warm khaddar fabric perfect for transition weather.',
            'colors': ['Maroon', 'Purple'], 'sizes': ['Standard'], 'image': 'products/unstitched-1.jpg'
        },

        # --- READY TO WEAR ---
        {
            'name': 'Daily Wear Printed Kurta',
            'category': rtw, 'price': '2,200', 'old_price': '3,500', 'discount_percent': 35, 'stock': 100,
            'badge': 'Best Seller', 'description': 'Comfortable cotton printed kurta for daily use.',
            'colors': ['White', 'Blue'], 'sizes': ['S', 'M', 'L', 'XL'], 'image': 'products/rtw-1.jpg'
        },
        {
            'name': 'Solid Silk Tunic',
            'category': rtw, 'price': '5,500', 'old_price': '7,000', 'discount_percent': 20, 'stock': 45,
            'badge': 'New', 'description': 'Pure silk solid color tunic with minimalist detailing.',
            'colors': ['Maroon', 'Black'], 'sizes': ['XS', 'S', 'M', 'L'], 'image': 'products/rtw-1.jpg'
        },
        {
            'name': 'Embroidered Velvet Kaftan',
            'category': rtw, 'price': '8,900', 'old_price': '11,000', 'discount_percent': 19, 'stock': 15,
            'badge': 'Luxe', 'description': 'Luxurious velvet kaftan with heavy gold embroidery.',
            'colors': ['Purple', 'Gold'], 'sizes': ['Standard'], 'image': 'products/rtw-1.jpg'
        },
        {
            'name': 'Linen Co-ord Set',
            'category': rtw, 'price': '4,500', 'old_price': '5,500', 'discount_percent': 18, 'stock': 35,
            'badge': 'Trending', 'description': 'Modern 2-piece linen co-ord set in trendy colors.',
            'colors': ['Teal', 'Maroon'], 'sizes': ['S', 'M', 'L'], 'image': 'products/rtw-1.jpg'
        },
        {
            'name': 'Cotton Net Formal Kurta',
            'category': rtw, 'price': '6,200', 'old_price': '8,000', 'discount_percent': 22, 'stock': 25,
            'badge': 'Elegant', 'description': 'Formal cotton net kurta with delicate lace work.',
            'colors': ['White', 'Gold'], 'sizes': ['XS', 'S', 'M', 'L'], 'image': 'products/rtw-1.jpg'
        },

        # --- LUXE EDITION ---
        {
            'name': 'Embroidered Chiffon Collection',
            'category': luxe, 'price': '12,500', 'old_price': '15,000', 'discount_percent': 15, 'stock': 20,
            'badge': 'Luxe', 'description': 'Exquisite hand-embroidered chiffon suite.',
            'colors': ['Black', 'Gold'], 'sizes': ['S', 'M', 'L'], 'image': 'products/luxe-1.jpg'
        },
        {
            'name': 'Handcrafted Organza Saree',
            'category': luxe, 'price': '18,000', 'old_price': '22,000', 'discount_percent': 18, 'stock': 10,
            'badge': 'Exclusive', 'description': 'Breathable organza saree with hand-painted motifs.',
            'colors': ['Pink', 'White'], 'sizes': ['Standard'], 'image': 'products/luxe-1.jpg'
        },
        {
            'name': 'Bridal Silk Lehenga',
            'category': luxe, 'price': '45,000', 'old_price': '55,000', 'discount_percent': 18, 'stock': 5,
            'badge': 'Bridal', 'description': 'Traditional bridal lehenga with intricate zardozi work.',
            'colors': ['Red', 'Gold'], 'sizes': ['M', 'L'], 'image': 'products/luxe-1.jpg'
        },
        {
            'name': 'Heavy Embroidered Net Pishwas',
            'category': luxe, 'price': '22,500', 'old_price': '28,000', 'discount_percent': 19, 'stock': 8,
            'badge': 'Luxe', 'description': 'Floor length net pishwas with mirror work details.',
            'colors': ['Maroon', 'Gold'], 'sizes': ['S', 'M', 'L'], 'image': 'products/luxe-1.jpg'
        },
        {
            'name': 'Premium Raw Silk Suit',
            'category': luxe, 'price': '15,500', 'old_price': '19,000', 'discount_percent': 18, 'stock': 12,
            'badge': 'New', 'description': 'Minimalist raw silk suit with statement sleeves.',
            'colors': ['Emerald Green', 'Black'], 'sizes': ['S', 'M', 'L'], 'image': 'products/luxe-1.jpg'
        },

        # --- ACCESSORIES ---
        {
            'name': 'Velvet Embroidered Clutch',
            'category': acc, 'price': '1,800', 'old_price': '2,500', 'discount_percent': 28, 'stock': 30,
            'badge': 'Limited', 'description': 'Elegant velvet clutch with gold embroidery.',
            'colors': ['Black', 'Maroon'], 'sizes': ['Standard'], 'image': 'products/acc-1.jpg'
        },
        {
            'name': 'Silk Scarf with Tassels',
            'category': acc, 'price': '1,200', 'old_price': '1,500', 'discount_percent': 20, 'stock': 50,
            'badge': 'New', 'description': 'Digital printed silk scarf with handmade tassels.',
            'colors': ['Pink', 'Blue'], 'sizes': ['Standard'], 'image': 'products/acc-1.jpg'
        },
        {
            'name': 'Pearl Embellished Potli Bag',
            'category': acc, 'price': '2,500', 'old_price': '3,200', 'discount_percent': 22, 'stock': 25,
            'badge': 'Handmade', 'description': 'Traditional potli bag covered in faux pearls.',
            'colors': ['White', 'Gold'], 'sizes': ['Standard'], 'image': 'products/acc-1.jpg'
        },
        {
            'name': 'Gold Plated Jewelry Set',
            'category': acc, 'price': '3,500', 'old_price': '4,500', 'discount_percent': 22, 'stock': 15,
            'badge': 'Elegant', 'description': 'Timeless gold plated necklace and earrings set.',
            'colors': ['Gold'], 'sizes': ['Standard'], 'image': 'products/acc-1.jpg'
        },
        {
            'name': 'Designer Leather Handbag',
            'category': acc, 'price': '7,500', 'old_price': '9,000', 'discount_percent': 16, 'stock': 10,
            'badge': 'Premium', 'description': 'Genuine leather handbag with spacious compartments.',
            'colors': ['Black', 'Maroon'], 'sizes': ['Standard'], 'image': 'products/acc-1.jpg'
        }
    ]

    for p in data:
        prod, created = Product.objects.update_or_create(
            name=p['name'],
            defaults={
                'category': p['category'],
                'price': p['price'],
                'old_price': p['old_price'],
                'discount_percent': p['discount_percent'],
                'stock': p['stock'],
                'badge': p['badge'],
                'description': p['description'],
                'image': p['image'],
                'wholesale_price': '3850' if int(p['price'].replace(',', '')) > 4000 else str(int(int(p['price'].replace(',', '')) * 0.85)),
                'wholesale_package_size': 6
            }
        )
        prod.available_colors.set([color_objs[c] for c in p['colors']])
        prod.available_sizes.set([size_objs[s] for s in p['sizes']])
        print(f"{'Created' if created else 'Updated'}: {prod.name}")

if __name__ == '__main__':
    populate_products()
    print("\nTotal 20 products populated successfully!")
