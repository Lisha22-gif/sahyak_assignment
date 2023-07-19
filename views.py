from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from pdfdocument import PDFDocument
from .models import Certificate

def generate_certificate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        course = request.POST.get('course')

        # Generate the certificate PDF using pdfdocument
        pdf = PDFDocument()
        pdf.init_report()
        pdf.h1('Certificate of Completion')
        pdf.h2('This certifies that')
        pdf.h2(name)
        pdf.h2('has successfully completed the course:')
        pdf.h2(course)
        pdf.generate()

        # Save the certificate as a PDF file
        pdf_filename = f'{name.replace(" ", "_")}_certificate.pdf'
        pdf_path = f'certificates/{pdf_filename}'
        pdf.save(pdf_path)

        # Generate JWT token for verification
        token = jwt.encode({'name': name, 'course': course}, 'secret_key', algorithm='HS256')

        # Save the certificate details and token in the database
        certificate = Certificate(name=name, course=course, token=token)
        certificate.save()

        return JsonResponse({'pdf_path': pdf_path, 'token': token.decode()})

    return render(request, 'generate_certificate.html')

def verify_certificate(request, token):
    try:
        # Verify the token using the secret key
        decoded = jwt.decode(token, 'secret_key', algorithms=['HS256'])

        # Retrieve the certificate details from the database
        certificate = Certificate.objects.get(token=token)

        return JsonResponse({'valid': True, 'data': decoded, 'certificate': certificate})

    except jwt.InvalidTokenError:
        return JsonResponse({'valid': False, 'error': 'Invalid token'})
    except Certificate.DoesNotExist:
        return JsonResponse({'valid': False, 'error': 'Certificate not found'})

def download_certificate(request, certificate_id):
    certificate = Certificate.objects.get(pk=certificate_id)
    file_path = certificate.pdf_path

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={certificate.name}_certificate.pdf'

    return response
