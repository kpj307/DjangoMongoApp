from django.urls import path
from .views import PDFUploadView, upload_form, display_nouns_verbs

urlpatterns = [
    path('api/', PDFUploadView.as_view(), name='file-upload'),
    path('', upload_form, name='upload-form'),
    path('display/', display_nouns_verbs, name='display-nouns-verbs'),
]
