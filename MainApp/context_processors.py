import os
from django.conf import settings


def media_env(request):
    return {
        'env_headshot_url': os.environ.get('PROFILE_HEADSHOT_URL', ''),
        'env_resume_url': os.environ.get('PROFILE_RESUME_URL', ''),
    }
