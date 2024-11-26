from django.db import models

# Create your models here.
from django.db import models

class UnauthorizedAccessLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    url_accessed = models.URLField()
    user_agent = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Unauthorized Access: {self.ip_address} at {self.timestamp}"



class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    blocked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blocked IP: {self.ip_address} at {self.blocked_at}"
