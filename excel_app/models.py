from django.db import models
from django.utils import timezone

# Create your models here.

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ['-uploaded_at']
