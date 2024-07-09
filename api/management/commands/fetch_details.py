import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Executes the scrape script to ingest the war thunder t details info into the DB"

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the t detail scraper...')
        result = subprocess.run(['python', 'api/management/scripts/scrape_details.py'], capture_output=True, text=True)
    
        if result.returncode == 0:
            self.stdout.write(self.style.SUCCESS('Successfully started fetch tournament details'))
            self.stdout.write(result.stdout)
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch t details'))
            self.stdout.write(result.stderr)