from django.contrib import admin
from .models import (
    Profile, PageContent, ExpertiseCard, Project, ProjectImage, Skill,
    ResumeSection, Appointment, ContactMessage,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline', 'email', 'location']
    fieldsets = [
        ('Identity', {'fields': ['name', 'tagline', 'bio', 'headshot']}),
        ('Contact', {'fields': ['email', 'phone', 'location']}),
        ('Social Links', {'fields': ['github', 'linkedin', 'twitter']}),
        ('Resume', {'fields': ['resume_summary', 'resume_pdf']}),
    ]


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ['page', 'section', 'title', 'is_active']
    list_filter = ['page', 'is_active']
    list_editable = ['is_active']
    search_fields = ['section', 'title', 'body']


@admin.register(ExpertiseCard)
class ExpertiseCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'link_url', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ['image', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ['title', 'is_featured', 'order', 'created_at']
    list_editable = ['is_featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'tools']
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'slug', 'short_description', 'description', 'tools', 'image', 'video']}),
        ('Project Details', {'fields': ['problem', 'key_features', 'solution', 'outcome']}),
        ('Your Contribution', {'fields': ['role', 'challenge', 'learnings']}),
        ('Links', {'fields': ['github_url', 'demo_url']}),
        ('Display', {'fields': ['order', 'is_featured']}),
    ]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'order']
    list_editable = ['proficiency', 'order']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(ResumeSection)
class ResumeSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'organization', 'start_date', 'end_date', 'order']
    list_editable = ['order']
    list_filter = ['type']
    search_fields = ['title', 'organization']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date', 'time', 'purpose', 'status', 'created_at']
    list_filter = ['status', 'date']
    list_editable = ['status']
    search_fields = ['name', 'email', 'purpose']
    readonly_fields = ['created_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
