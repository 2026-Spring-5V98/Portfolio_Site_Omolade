"""
Restores Profile headshot and resume_pdf from environment variables on each deploy.

After uploading your headshot and resume via Django admin, find the Cloudinary
path in the admin "Currently:" link (e.g. media/profile/headshot.jpg) and set:
  PROFILE_HEADSHOT=media/profile/your-headshot.jpg
  PROFILE_RESUME_PDF=resume/your-resume.pdf
in the Render dashboard → Environment tab.

This command then runs every deploy and restores the paths if the DB was reset.
"""
import os

from django.core.management.base import BaseCommand

from MainApp.models import Profile


class Command(BaseCommand):
    help = 'Restore Profile media paths from PROFILE_HEADSHOT / PROFILE_RESUME_PDF env vars'

    def handle(self, *args, **options):
        profile = Profile.objects.first()
        if not profile:
            self.stdout.write('  No Profile found — skipping media sync.')
            return

        headshot_path = os.environ.get('PROFILE_HEADSHOT', '').strip()
        resume_path = os.environ.get('PROFILE_RESUME_PDF', '').strip()

        changed = False

        if headshot_path and not profile.headshot:
            profile.headshot = headshot_path
            changed = True
            self.stdout.write(f'  Restored headshot: {headshot_path}')

        if resume_path and not profile.resume_pdf:
            profile.resume_pdf = resume_path
            changed = True
            self.stdout.write(f'  Restored resume_pdf: {resume_path}')

        if changed:
            profile.save()
            self.stdout.write(self.style.SUCCESS('  Profile media paths restored.'))
        else:
            self.stdout.write('  Media paths already set — nothing to restore.')
