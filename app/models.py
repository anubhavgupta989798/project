from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=[
        ('TECHNICAL', 'Technical Issue'),
        ('SERVICE', 'Service Complaint'),
        ('BILLING', 'Billing Problem'),
        ('OTHER', 'Other')
    ])
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ("Approved","Approved"),
        ('RESOLVED', 'Resolved')
    ], default='PENDING') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Check if this is an existing complaint
        if self.pk:
            orig = Complaint.objects.get(pk=self.pk)
            # Check if assigned_user has changed
            if orig.assigned_user != self.assigned_user:
                # Send email if a new user is assigned
                if self.assigned_user:
                    send_mail(
                        'New Complaint Assigned',
                        f'You have been assigned to handle the complaint: {self.title}',
                        settings.DEFAULT_FROM_EMAIL,
                        [self.assigned_user]
                    )
        
        # Call the original save method
        super().save(*args, **kwargs)