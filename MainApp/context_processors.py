import os


def media_env(request):
    headshot_url = os.environ.get('PROFILE_HEADSHOT_URL', '')
    resume_url = os.environ.get('PROFILE_RESUME_URL', '')

    if not headshot_url:
        try:
            from django.contrib.staticfiles.storage import staticfiles_storage
            headshot_url = staticfiles_storage.url('MainApp/img/headshot.jpg')
        except Exception:
            pass

    if not resume_url:
        try:
            from django.contrib.staticfiles.storage import staticfiles_storage
            resume_url = staticfiles_storage.url('MainApp/files/resume.pdf')
        except Exception:
            pass

    return {
        'env_headshot_url': headshot_url,
        'env_resume_url': resume_url,
    }
