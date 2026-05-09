from django.db import models
from django.utils.text import slugify


def _resume_storage():
    from django.conf import settings
    if getattr(settings, 'USE_CLOUDINARY', False):
        from cloudinary_storage.storage import RawMediaCloudinaryStorage
        return RawMediaCloudinaryStorage()
    from django.core.files.storage import FileSystemStorage
    return FileSystemStorage()


class Profile(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    bio = models.TextField()
    headshot = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    resume_summary = models.TextField(blank=True)
    resume_pdf = models.FileField(
        upload_to='resume/',
        blank=True,
        null=True,
        storage=_resume_storage,
        help_text='Upload your resume as a PDF file for public download.',
    )

    class Meta:
        verbose_name = 'Profile'

    def __str__(self):
        return self.name


class PageContent(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('about', 'About'),
        ('projects', 'Projects'),
        ('skills', 'Skills'),
        ('resume', 'Resume'),
        ('contact', 'Contact'),
    ]
    page = models.CharField(max_length=20, choices=PAGE_CHOICES)
    section = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', 'section']
        verbose_name = 'Page Content'
        verbose_name_plural = 'Page Contents'

    def __str__(self):
        return f"{self.page} — {self.section}"


class ExpertiseCard(models.Model):
    icon = models.CharField(
        max_length=10, default='💡',
        help_text='Paste an emoji e.g. 💡 🖥️ 📊 🤖 🔧'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    link_text = models.CharField(max_length=60, default='Learn More →')
    link_url = models.CharField(max_length=200, default='/projects/',
        help_text='Relative URL e.g. /projects/ or /skills/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Expertise Card'
        verbose_name_plural = 'Expertise Cards'

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    tools = models.CharField(max_length=500, help_text='Comma-separated list of tools/technologies')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    video = models.FileField(upload_to='projects/videos/', blank=True, null=True,
                             help_text='Upload a demo video (MP4 recommended)')
    problem = models.TextField(blank=True, verbose_name='Business Problem')
    solution = models.TextField(blank=True)
    outcome = models.TextField(blank=True, verbose_name='Outcome / Results')
    key_features = models.TextField(blank=True, verbose_name='Key Features',
                                    help_text='One feature per line')
    role = models.TextField(blank=True, verbose_name='Your Role / Contribution')
    challenge = models.TextField(blank=True, verbose_name='Biggest Challenge')
    learnings = models.TextField(blank=True, verbose_name='What You Learned')
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_tools_list(self):
        return [t.strip() for t in self.tools.split(',') if t.strip()]

    def get_features_list(self):
        return [f.strip() for f in self.key_features.split('\n') if f.strip()]

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    def __str__(self):
        return f"{self.project.title} — image {self.order}"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('languages', 'Programming Languages'),
        ('frameworks', 'Frameworks & Libraries'),
        ('ai_ml', 'AI & Machine Learning'),
        ('tools', 'Tools & Platforms'),
        ('databases', 'Databases'),
        ('soft_skills', 'Soft Skills'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.PositiveSmallIntegerField(
        default=3,
        choices=[(i, i) for i in range(1, 6)],
        help_text='1 (Beginner) to 5 (Expert)',
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def proficiency_percent(self):
        return self.proficiency * 20

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class ResumeSection(models.Model):
    TYPE_CHOICES = [
        ('education', 'Education'),
        ('experience', 'Experience'),
        ('certification', 'Certification'),
        ('achievement', 'Achievement'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True, help_text='Leave blank for "Present"')
    description = models.TextField(blank=True)
    bullet_points = models.TextField(blank=True, help_text='One bullet point per line')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['type', 'order', '-start_date']
        verbose_name = 'Resume Section'

    def get_bullets(self):
        if self.bullet_points:
            return [b.strip() for b in self.bullet_points.split('\n') if b.strip()]
        return []

    def date_range(self):
        if self.start_date and self.end_date:
            return f"{self.start_date} – {self.end_date}"
        if self.start_date:
            return f"{self.start_date} – Present"
        return ""

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateField()
    time = models.TimeField()
    purpose = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    calendar_event_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.date} {self.time}"


class SiteVisit(models.Model):
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Site Visit'

    def __str__(self):
        return f"{self.ip_address} — {self.path}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'

    def __str__(self):
        return f"{self.name}: {self.subject}"
