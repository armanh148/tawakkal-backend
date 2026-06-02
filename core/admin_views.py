import os
from google import genai
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Product, Category, Color, Size
import json

# Replace with your actual Gemini API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
client = genai.Client(api_key=GEMINI_API_KEY)

class SmartAddForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'Paste product description here (e.g., from a website)...'}),
        help_text="Paste the product details and AI will try to extract the fields."
    )

def smart_add_product(request):
    if request.method == 'POST':
        form = SmartAddForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            
            try:
                prompt = f"""
                Extract product details from the following text and return ONLY a JSON object.
                If a field is missing, use null.
                Fields: name, price (include PKR), badge (e.g., New, Best Seller), description, category, colors (list), sizes (list).
                
                Text: {description}
                """
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                )
                
                # Try to find JSON in the response
                text_response = response.text
                json_start = text_response.find('{')
                json_end = text_response.rfind('}') + 1
                data = json.loads(text_response[json_start:json_end])
                
                # Build the query string for the Django admin "Add" form
                # Note: Many-to-Many and ForeignKeys are tricky with initial values in URL, 
                # but we can pass basic fields and try to handle the rest.
                
                admin_add_url = reverse('admin:core_product_add')
                params = []
                if data.get('name'): params.append(f"name={data['name']}")
                if data.get('price'): params.append(f"price={data['price']}")
                if data.get('badge'): params.append(f"badge={data['badge']}")
                if data.get('description'): params.append(f"description={data['description']}")
                
                # For category, we might need the ID, but for now let's just use what we have
                
                final_url = f"{admin_add_url}?{'&'.join(params)}"
                
                # Store extra data (colors, sizes, category name) in session to help user
                request.session['ai_extracted_data'] = data
                
                return redirect(final_url)
                
            except Exception as e:
                messages.error(request, f"AI Error: {str(e)}")
                # Fallback: if API fails, just show the form again or provide a mock
    else:
        form = SmartAddForm()
        
    return render(request, 'admin/smart_add.html', {'form': form, 'title': 'AI Smart Add'})
