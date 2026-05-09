"""
Dumps the current database state to initial_data.json.

Run this from the Render Shell after uploading new images/content via admin:
    python manage.py dump_fixture

Then copy MainApp/fixtures/initial_data.json from the Render shell output,
paste it into your local file, and push to GitHub so the data survives
any future database resets.
"""
from django.core import serializers
from django.core.management.base import BaseCommand
from pathlib import Path

from MainApp.models import (
    Profile, PageContent, ExpertiseCard,
    Project, Skill, ResumeSection,
)


class Command(BaseCommand):
    help = 'Dump current DB state to MainApp/fixtures/initial_data.json'

    def handle(self, *args, **options):
        objects = (
            list(Profile.objects.all()) +
            list(PageContent.objects.all()) +
            list(ExpertiseCard.objects.all()) +
            list(Project.objects.all()) +
            list(Skill.objects.all()) +
            list(ResumeSection.objects.all())
        )

        data = serializers.serialize('json', objects, indent=2)

        fixture_path = Path(__file__).resolve().parents[3] / 'fixtures' / 'initial_data.json'
        fixture_path.write_text(data, encoding='utf-8')

        self.stdout.write(self.style.SUCCESS(f'Fixture saved → {fixture_path}'))
        self.stdout.write('\n--- COPY EVERYTHING BELOW THIS LINE ---\n')
        self.stdout.write(data)
        self.stdout.write('\n--- END ---')
