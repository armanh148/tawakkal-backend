import re
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from core.models import TikTokReel, SiteSettings

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


def get_username(profile_url):
    match = re.search(r'@([a-zA-Z0-9._-]+)', profile_url)
    return match.group(1) if match else profile_url.strip('@').strip('/')


def fetch_oembed(video_url):
    """Get thumbnail URL + title from TikTok's free oEmbed endpoint."""
    try:
        resp = requests.get(
            'https://www.tiktok.com/oembed',
            params={'url': video_url},
            timeout=15,
            headers=HEADERS,
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


def download_image(url, filename):
    """Download image bytes — returns ContentFile or None."""
    try:
        resp = requests.get(url, timeout=20, headers=HEADERS)
        if resp.status_code == 200 and resp.content:
            return ContentFile(resp.content, name=filename)
    except Exception:
        pass
    return None


class Command(BaseCommand):
    help = (
        'Refresh TikTok reels in the database.\n'
        'For each active reel it re-fetches the thumbnail via TikTok oEmbed '
        'and saves the image locally so it never expires.\n\n'
        'To ADD new reels go to:\n'
        '  Admin → TikTok Reels → "Bulk Import from TikTok URLs" button'
    )

    def handle(self, *args, **options):
        site = SiteSettings.objects.first()
        if not site or not site.tiktok_sync_active:
            self.stdout.write(self.style.WARNING(
                'TikTok sync is disabled or Site Settings not found.\n'
                'Enable "Tiktok sync active" in Admin → Site Settings.'
            ))
            return

        reels = TikTokReel.objects.filter(is_active=True)
        if not reels.exists():
            self.stdout.write(self.style.WARNING(
                'No active reels found.\n'
                'Go to Admin → TikTok Reels → "Bulk Import from TikTok URLs" '
                'and paste your video links there.'
            ))
            return

        self.stdout.write(f'Refreshing thumbnails for {reels.count()} reel(s)...\n')
        ok, fail = 0, 0

        for reel in reels:
            oembed = fetch_oembed(reel.video_url)
            if not oembed or not oembed['thumbnail_url']:
                self.stdout.write(self.style.ERROR(f'  FAIL {reel.video_id} — oEmbed returned nothing'))
                fail += 1
                continue

            img_file = download_image(
                oembed['thumbnail_url'],
                f'{reel.video_id}.jpg',
            )
            if img_file:
                reel.cover_image.save(f'{reel.video_id}.jpg', img_file, save=False)
                reel.cover_image_url = oembed['thumbnail_url']
                if not reel.title and oembed['title']:
                    reel.title = oembed['title']
                reel.save()
                self.stdout.write(self.style.SUCCESS(f'  OK  {reel.video_id}'))
                ok += 1
            else:
                # Fallback: at least store the CDN URL even without local copy
                reel.cover_image_url = oembed['thumbnail_url']
                reel.save()
                self.stdout.write(f'  ~   {reel.video_id} — URL saved, image download failed')
                ok += 1

        self.stdout.write(self.style.SUCCESS(f'\nDone: {ok} refreshed, {fail} failed.'))
