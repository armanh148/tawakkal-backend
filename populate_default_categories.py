import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Category

categories = [
    {
        'name': 'Unstitched',
        'image': 'categories/unstitched.jpg',
    },
    {
        'name': 'Ready to Wear',
        'image': 'categories/ready to wear.webp',
    },
    {
        'name': 'Luxe Edition',
        'image': 'categories/Luxe edition.webp',
    },
    {
        'name': 'Accessories',
        'image': 'categories/accessories.jpg',
    }
]

for cat_data in categories:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'image': cat_data['image'], 'is_published': True}
    )
    if created:
        print(f"Created category: {category.name}")
    else:
        # Update existing to ensure images match
        category.image = cat_data['image']
        category.save()
        print(f"Updated category: {category.name}")

print("Done!")
