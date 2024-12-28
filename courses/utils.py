import logging
from datetime import datetime
from PIL import Image
from PIL import UnidentifiedImageError
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.conf import settings
import os
from django.core.files import File

logger = logging.getLogger(__name__)


def create_certificate(user, course):


    from .models import Certificate, CourseProgress  # Import models here

    try:
        certificates_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
        if not os.path.exists(certificates_dir):
            os.makedirs(certificates_dir)

        certificate_filename = f"{user.username}_{course.id}_certificate.pdf"
        certificate_filepath = os.path.join(certificates_dir, certificate_filename)

        c = canvas.Canvas(certificate_filepath, pagesize=letter)
        c.setFont("Helvetica", 24)
        c.drawString(100, 650, "Certificate of Completion")
        c.setFont("Helvetica", 20)
        c.drawString(100, 600, f"Presented to {user.username}")
        c.drawString(100, 550, f"Course: {course.title}")
        c.drawString(100, 500, f"Date of Completion: {datetime.now().strftime('%Y-%m-%d')}")

        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
        try:
            img = Image.open(logo_path)
            # Используйте объект img для дальнейшей обработки изображения
            # Например, для создания миниатюры:
            img.thumbnail((100, 100))
            # Сохранение измененного изображения:
            img.save('new_logo.jpg')
        except FileNotFoundError:
            print("Файл изображения не найден")
        except IOError:
            print("Ошибка при открытии файла изображения")


        with open(certificate_filepath, 'rb') as f:
            file = File(f)
            certificate = Certificate.objects.create(user=user, course=course, pdf_file=file)

        return certificate
    except Exception as e:
        logger.error(f"Error generating certificate: {e}")
        logger.error(f"Logo path: {logo_path}")
        raise


def update_progress(user, course, part):

    from .models import CourseProgress  # Import model here

    progress, created = CourseProgress.objects.get_or_create(user=user, course=course, part=part)
    if not progress.video_watched:
        progress.video_watched = True
        progress.save()