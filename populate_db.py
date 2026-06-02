import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import Category, Product

def populate():
    if not os.path.exists('products.json'):
        print("products.json not found!")
        return

    with open('products.json', 'r') as f:
        products = json.load(f)

    for p in products:
        cat_name = p.get('category', 'Uncategorized')
        cat, created = Category.objects.get_or_create(name=cat_name)
        
        Product.objects.create(
            name=p['name'],
            category=cat,
            price=p['price'],
            image=p['image'],
            link=p['link'],
            badge=p.get('badge')
        )

    print(f"Database populated with {len(products)} products successfully!")

if __name__ == '__main__':
    populate()
