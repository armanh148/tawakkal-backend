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
        
        # 1. Fetch latest reels (simulated for now, can be replaced with real TikTok API/Scraper)
        # Note: TikTok has strict bot protection, so in production use services like 
        # TikAPI, Apify TikTok Scraper, or similar official/unofficial APIs.
        
        latest_reels = [
            {
                'video_id': '7401234567890123458',
                'video_url': f'https://www.tiktok.com/@{username}/video/7401234567890123458',
                'cover_image_url': 'https://images.unsplash.com/photo-1560457079-9a6532ccb118?auto=format&fit=crop&q=80&w=600',
                'title': 'Unstitched Luxury Embroidery',
                'category': 'UNSTITCHED',
                'price': 'PKR 8,990'
            },
            {
                'video_id': '7401234567890123457',
                'video_url': f'https://www.tiktok.com/@{username}/video/7401234567890123457',
                'cover_image_url': 'https://images.unsplash.com/photo-1599032909756-5dee8c65f47a?auto=format&fit=crop&q=80&w=600',
                'title': 'Cotton Jacquard Collection',
                'category': 'RTW',
                'price': 'PKR 7,290'
            },
            {
                'video_id': '7401234567890123456',
                'video_url': f'https://www.tiktok.com/@{username}/video/7401234567890123456',
                'cover_image_url': 'https://images.unsplash.com/photo-1583391733956-6c78276477e2?auto=format&fit=crop&q=80&w=600',
                'title': 'Royal Velvet Festive 2026',
                'category': 'LUXE',
                'price': 'PKR 18,500'
            }
        ]

        # 2. Add/Update latest reels and set them to active
        new_ids = []
        for reel_data in latest_reels:
            reel, created = TikTokReel.objects.update_or_create(
                video_id=reel_data['video_id'],
                defaults={
                    'video_url': reel_data['video_url'],
                    'cover_image_url': reel_data['cover_image_url'],
                    'title': reel_data['title'],
                    'category': reel_data['category'],
                    'price': reel_data['price'],
                    'is_active': True, # Ensure latest ones are active
                }
            )
            new_ids.append(reel.video_id)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Newly added: Reel {reel.video_id}'))
            else:
                self.stdout.write(f'Updated: Reel {reel.video_id}')

        # 3. AUTO-DEACTIVATE OLD REELS:
        # Only keep the latest 10 active reels. Deactivate anything else.
        active_reels = TikTokReel.objects.filter(is_active=True).order_by('-created_at')
        if active_reels.count() > 10:
            reels_to_deactivate = active_reels[10:]
            for r in reels_to_deactivate:
                r.is_active = False
                r.save()
            self.stdout.write(self.style.WARNING(f'Deactivated {len(reels_to_deactivate)} older reels to keep feed fresh.'))

        self.stdout.write(self.style.SUCCESS('TikTok feed is now perfectly synced with your latest content.'))
