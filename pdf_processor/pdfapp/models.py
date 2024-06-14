from djongo import models

class PDFFile(models.Model):
    email = models.EmailField(unique=True)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    nouns = models.TextField(blank=True)
    verbs = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]
