from django.core.management.base import BaseCommand
from django.core.management import call_command
from MainApp.models import Profile


class Command(BaseCommand):
    help = 'Load initial fixture data only if the database is empty.'

    def handle(self, *args, **options):
        if Profile.objects.exists():
            self.stdout.write('Data already loaded — skipping.')
            return
        call_command('loaddata', 'MainApp/fixtures/initial_data.json')
        self.stdout.write('Initial data loaded.')
