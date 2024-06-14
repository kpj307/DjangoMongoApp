import io
import nltk
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from PyPDF2 import PdfReader
from .models import PDFFile
from .serializers import PDFFileSerializer

class PDFUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = PDFFileSerializer(data=request.data)
        if file_serializer.is_valid():
            pdf_file = request.FILES['file']
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()

            words = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(words)
            nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
            verbs = [word for word, pos in pos_tags if pos.startswith('VB')]

            file_serializer.save(nouns=" ".join(nouns), verbs=" ".join(verbs))
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def upload_form(request):
    return render(request, 'upload.html')

def display_nouns_verbs(request):
    files = PDFFile.objects.all()
    context = {
        'files': files
    }
    return render(request, 'display_nouns_verbs.html', context)
