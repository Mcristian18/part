from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


studData = {
	"studentNum": "202012632",
	"student": "MARK CRISTIAN" + " " + "QUIAZON",

	"courseCode": "123 Street name",
	"courseName": "Vancouver",
	"units": "3",
	"grade": "98663",
	"remarks": "",

	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('app/pdf_template.html', studData)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('app/pdf_template.html', studData)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Grades_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response



def index(request):
	context = {}
	return render(request, 'app/index.html', context)