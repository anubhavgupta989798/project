from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('user', 'title', 'category', 'status', 'created_at','assigned_user')
    
    # Fields to use for filtering
    list_filter = ('status', 'category', 'created_at')
    
    # Fields to search through
    search_fields = ('title', 'description', 'user__username')
    
    # Make certain fields read-only
    readonly_fields = ('user', 'created_at', 'updated_at','category')
    
    # Group fields in the edit view
    fieldsets = (
        ('Complaint Details', {
            'fields': ('user', 'title', 'description', 'category','assigned_user')
        }),
        ('Status Information', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )