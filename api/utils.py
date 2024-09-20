import csv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate_csv(data, filename):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(data['headers'])
    for row in data['rows']:
        writer.writerow(row)

    return response


def generate_pdf(data, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    _, height = letter

    y = height - 40
    for header in data['headers']:
        p.drawString(30, y, header)
        y -= 20

    y -= 20
    for row in data['rows']:
        for item in row:
            p.drawString(30, y, str(item))
            y -= 20
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response.write(buffer.getvalue())
    return response
