from django.shortcuts import render
from django.http.response import HttpResponse

from . models import myuploadfile

from names_dataset import NameDataset 
from names_dataset import NameDatasetV1 

import nltk


from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import glob
import os

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from pdf.serializers import MyUploadFileSerializer

def home(request):
    return render(request, "index.html",)

@csrf_exempt
def Upload(request):
    if request.method == "POST":

        files=os.listdir("media")
        for i in range(0,len(files)):
            os.remove("media"+'/'+files[i])
        
        
        myfile = request.FILES.getlist("files")

        for f in myfile:
            myuploadfile(myfiles=f).save()
        dossier = glob.glob("media/*")
        
        for j in dossier:
            
            output_string = StringIO()
            with open(j, 'rb') as in_file:
                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                rsrcmgr = PDFResourceManager()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)
                text = output_string.getvalue()

                
                table_mot=[]
                text_tokenize = nltk.word_tokenize(text)
                text_tokenize
                text_to_string = " "
                for text in text_tokenize:
                    text_to_string += text + " "
                text_tagged = nltk.pos_tag(text_tokenize)
                for text in text_tagged:
                    if text[1]=='NNP':
                        table_mot.append(text[0])


                m=NameDatasetV1()
                mot_cherche = []
                for tbl in table_mot:
                    if m.search_first_name(tbl):
                        mot_cherche.append(tbl)
                print("mot_cherche  ", mot_cherche)
        return render(request,'index.html')
        


