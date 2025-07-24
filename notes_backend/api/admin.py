from django.contrib import admin
from .models import Note

# PUBLIC_INTERFACE
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin view for Note model."""
    list_display = ["id", "title", "user", "created_at", "updated_at"]
    search_fields = ["title", "content", "user__username"]
    list_filter = ["user"]

