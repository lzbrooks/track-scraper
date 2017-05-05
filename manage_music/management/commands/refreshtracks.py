from django.core.management.base import BaseCommand
from manage_music.cron import refresh_favourite_tracks


class Command(BaseCommand):
    help = 'Refreshes favourite tracks'

    def handle(self, *args, **options):
        refresh_favourite_tracks()
        self.stdout.write(self.style.SUCCESS('Successfully refreshed favourite tracks'))
