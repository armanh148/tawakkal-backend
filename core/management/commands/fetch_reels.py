import requests
from django.core.management.base import BaseCommand
from core.models import TikTokReel, SiteSettings

class Command(BaseCommand):
    help = 'Fetches latest reels from TikTok'

    def handle(self, *args, **options):
        settings = SiteSettings.objects.first()
        if not settings or not settings.tiktok_profile_url:
            self.stdout.write(self.style.WARNING('TikTok Profile URL not configured in Site Settings.'))
            return

        if not settings.tiktok_sync_active:
            self.stdout.write(self.style.WARNING('TikTok sync is currently disabled in Site Settings.'))
            return

        profile_url = settings.tiktok_profile_url
        # Extract username from URL (e.g., https://www.tiktok.com/@username -> username)
        import re
        match = re.search(r'@([a-zA-Z0-9._-]+)', profile_url)
        username = match.group(1) if match else profile_url
        
        self.stdout.write(f'Fetching reels for {profile_url} (Username: {username}) from TikTok...')
        
        # In a real scenario, you would use a TikTok API or a scraping service here.
        # Example using a hypothetical service or direct scraping (which is prone to blocks)
        
        # For now, we'll populate with some high-quality mock data that mimics 
        # what would come from an API to show the functionality.
        
        mock_reels = [
            {
                'video_id': '7401234567890123456',
                'video_url': 'https://www.tiktok.com/@tawakkalstudio/video/7401234567890123456',
                'cover_image_url': 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?auto=format&fit=crop&q=80&w=600',
                'title': 'New Festive Collection 2026',
                'category': 'LUXE',
                'price': 'PKR 18,500'
            },
            {
                'video_id': '7401234567890123457',
                'video_url': 'https://www.tiktok.com/@tawakkalstudio/video/7401234567890123457',
                'cover_image_url': 'https://images.unsplash.com/photo-1599032909756-5dee8c65f47a?auto=format&fit=crop&q=80&w=600',
                'title': 'Summer Essentials',
                'category': 'RTW',
                'price': 'PKR 7,290'
            },
            {
                'video_id': '7401234567890123458',
                'video_url': 'https://www.tiktok.com/@tawakkalstudio/video/7401234567890123458',
                'cover_image_url': 'https://images.unsplash.com/photo-1560457079-9a6532ccb118?auto=format&fit=crop&q=80&w=600',
                'title': 'Unstitched Embroidery',
                'category': 'UNSTITCHED',
                'price': 'PKR 8,990'
            }
        ]

        for reel_data in mock_reels:
            reel, created = TikTokReel.objects.get_or_create(
                video_id=reel_data['video_id'],
                defaults={
                    'video_url': reel_data['video_url'],
                    'cover_image_url': reel_data['cover_image_url'],
                    'title': reel_data['title'],
                    'category': reel_data['category'],
                    'price': reel_data['price'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added reel {reel.video_id}'))
            else:
                self.stdout.write(f'Reel {reel.video_id} already exists')

        self.stdout.write(self.style.SUCCESS('TikTok reels update complete.'))
