import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Executes the scrape script to ingest the war thunder tournaments info into the DB"

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the tournament scraper...')
        result = subprocess.run(['python', 'api/management/scripts/scrape_tournaments.py'], capture_output=True, text=True)
    
        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS('Successfully started fetched tournaments.'))
            self.stdout.write(result.stdout)
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch tournaments.'))
            self.stdout.write(result.stderr)