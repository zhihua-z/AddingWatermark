# pip install reportlab
# pip install PyPDF2

import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
import PyPDF2

shezhi = open('setting.txt', 'r')
data = shezhi.readlines()
filename = data[0].strip()
numberOfCopies = int(data[1].strip())
foreafterstr = ['', '']

formatstr = ''
if len(data) >= 3:
  formatstr = data[2].strip()
  foreafterstr = formatstr.split('xxx')

tempfolder = 'temp/'
outfolder = 'output/'

print(foreafterstr)

def PDFrotate(origFileName, newFileName, rotation):
  pdfFileObj = open(origFileName, 'rb')

  pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  pdfWriter = PyPDF2.PdfFileWriter()

  pageObj = pdfReader.getPage(0)

  transformation = PyPDF2.Transformation().rotate(rotation)

  pageObj.add_transformation(transformation)

  pdfWriter.addPage(pageObj)

  newFile = open(newFileName, 'wb')

  pdfWriter.write(newFile)

  pdfFileObj.close()
  newFile.close()


def MakePdf(filename, watermarkid):
  watermark = ' '.join([foreafterstr[0] + str(watermarkid) + foreafterstr[1] for x in range(30)])

  pdf = canvas.Canvas(filename)

  text = pdf.beginText(0, 0)
  text.setFont("Courier", 36)
  text.setFillColor('lightgrey')

  text.textLine(watermark)

  pdf.drawText(text)

  pdf.save()


def AddWatermark(filename, watermarkname, outfilename):

  input_file = open(filename, 'rb')
  input_pdf = PyPDF2.PdfFileReader(input_file)

  watermark_file = open(watermarkname, 'rb')
  watermark_pdf = PyPDF2.PdfFileReader(watermark_file)
  output = PyPDF2.PdfFileWriter()

  for i in range(input_pdf.getNumPages()):
    pdf_page = input_pdf.getPage(i)

    watermark_page = watermark_pdf.getPage(0)

    pdf_page.mergePage(watermark_page)
    output.addPage(pdf_page)

  merged_file = open(outfilename, 'wb')
  output.write(merged_file)

  merged_file.close()
  watermark_file.close()
  input_file.close()

for i in range(1, numberOfCopies + 1):
  outfilename = outfolder + filename[:len(filename) - 4] + str(i) + '.pdf'
  watermarkname = tempfolder + str(i) + '.pdf'

  print("generating", outfilename)

  MakePdf(watermarkname, i)
  PDFrotate(watermarkname, watermarkname, 45)

  AddWatermark(filename, watermarkname, outfilename)
