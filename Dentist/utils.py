"""
✅ Utility functions for the Dentist app
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Sum
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


# ============= EMAIL FUNCTIONS =============

def send_appointment_notification(appointment):
    """
    ✅ Qabulga yozilish haqida email yuborish
    """
    try:
        subject = f"Qabulga yozilish tasdiqlandi - {appointment.date}"

        # HTML template
        html_content = render_to_string('emails/appointment_confirmation.html', {
            'appointment': appointment,
            'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
        })

        # Text version
        text_content = strip_tags(html_content)

        # Email yaratish
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[appointment.email],
        )
        email.attach_alternative(html_content, "text/html")

        # Yuborish
        email.send()

        logger.info(f"Appointment notification sent to {appointment.email}")
        return True

    except Exception as e:
        logger.error(f"Error sending appointment notification: {str(e)}")
        return False


def send_contact_notification(contact_message):
    """
    ✅ Kontakt xabari haqida email yuborish
    """
    try:
        subject = f"Yangi xabar: {contact_message.subject}"

        html_content = render_to_string('emails/contact_notification.html', {
            'message': contact_message,
        })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],  # Adminlarga
            reply_to=[contact_message.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(f"Contact notification sent for message from {contact_message.email}")
        return True

    except Exception as e:
        logger.error(f"Error sending contact notification: {str(e)}")
        return False


def send_appointment_reminder(appointment):
    """
    ✅ Qabul eslatmasi yuborish (1 kun oldin)
    """
    try:
        subject = f"Eslatma: Sizning qabulingiz ertaga - {appointment.date}"

        html_content = render_to_string('emails/appointment_reminder.html', {
            'appointment': appointment,
        })

        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[appointment.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(f"Appointment reminder sent to {appointment.email}")
        return True

    except Exception as e:
        logger.error(f"Error sending appointment reminder: {str(e)}")
        return False


# ============= IMAGE PROCESSING =============

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def compress_image(image_file, max_size=(1920, 1080), quality=85):
    """
    ✅ Rasmni compress qilish va optimizatsiya
    """
    try:
        # Rasmni ochish
        img = Image.open(image_file)

        # EXIF orientatsiyasini tuzatish
        if hasattr(img, '_getexif'):
            exif = img._getexif()
            if exif is not None:
                orientation = exif.get(274)
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

        # RGB ga o'tkazish (agar RGBA bo'lsa)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background

        # Resize qilish (agar katta bo'lsa)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # BytesIO ga saqlash
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)

        # InMemoryUploadedFile yaratish
        compressed_file = InMemoryUploadedFile(
            output,
            'ImageField',
            f"{image_file.name.split('.')[0]}.jpg",
            'image/jpeg',
            sys.getsizeof(output),
            None
        )

        return compressed_file

    except Exception as e:
        logger.error(f"Error compressing image: {str(e)}")
        return image_file


# ============= CACHE HELPERS =============

def get_or_set_cache(key, callable_func, timeout=300):
    """
    ✅ Cache dan olish yoki yangilash
    """
    data = cache.get(key)
    if data is None:
        data = callable_func()
        cache.set(key, data, timeout)
    return data


def invalidate_cache_pattern(pattern):
    """
    ✅ Pattern bo'yicha cache tozalash
    """
    try:
        keys = cache.keys(pattern)
        if keys:
            cache.delete_many(keys)
            logger.info(f"Invalidated {len(keys)} cache keys matching pattern: {pattern}")
    except Exception as e:
        logger.error(f"Error invalidating cache pattern: {str(e)}")


# ============= VALIDATION HELPERS =============

import re


def validate_phone_number(phone):
    """
    ✅ O'zbekiston telefon raqamini tekshirish
    """
    phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    pattern = r'^\+998(9[012345789]|6[125679]|7[01234569])\d{7}$'
    return bool(re.match(pattern, phone))


def sanitize_filename(filename):
    """
    ✅ Fayl nomini tozalash
    """
    # Faqat a-z, 0-9, dash va underscore qoldirish
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.lower()


# ============= SLUG HELPERS =============

from django.utils.text import slugify as django_slugify


def unique_slug_generator(instance, new_slug=None, slug_field='slug'):
    """
    ✅ Unique slug yaratish
    """
    if new_slug is not None:
        slug = new_slug
    else:
        # Ingliz nomidan slug yaratish
        if hasattr(instance, 'name_en'):
            slug = django_slugify(instance.name_en)
        elif hasattr(instance, 'title_en'):
            slug = django_slugify(instance.title_en)
        else:
            slug = django_slugify(str(instance))

    # Agar bo'sh bo'lsa, random slug
    if not slug:
        import uuid
        slug = str(uuid.uuid4())[:8]

    # Unique qilish
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(**{slug_field: slug}).exists()

    if qs_exists:
        new_slug = f"{slug}-{instance.__class__.__name__.lower()}-{instance.pk or 'new'}"
        return unique_slug_generator(instance, new_slug=new_slug, slug_field=slug_field)

    return slug


# ============= DATE HELPERS =============

from datetime import datetime, timedelta
from django.utils import timezone


def get_working_days(start_date, end_date):
    """
    ✅ Ish kunlarini hisoblash (Yakshanbasiz)
    """
    working_days = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() != 6:  # 6 = Sunday
            working_days += 1
        current_date += timedelta(days=1)

    return working_days


def get_available_time_slots(date, doctor=None):
    """
    ✅ Bo'sh vaqt slotlarini olish
    """
    from .models import Appointment

    # Barcha mumkin bo'lgan vaqtlar (09:00 - 20:00, har 15 daqiqa)
    start_time = datetime.strptime('09:00', '%H:%M').time()
    end_time = datetime.strptime('20:00', '%H:%M').time()
    lunch_start = datetime.strptime('13:00', '%H:%M').time()
    lunch_end = datetime.strptime('14:00', '%H:%M').time()

    available_slots = []
    current_time = start_time

    while current_time < end_time:
        # Tushlik vaqti skip
        if not (lunch_start <= current_time < lunch_end):
            # Band vaqtlarni tekshirish
            is_booked = Appointment.objects.filter(
                date=date,
                time=current_time,
                doctor=doctor,
                status__in=['pending', 'confirmed']
            ).exists()

            if not is_booked:
                available_slots.append(current_time)

        # 15 daqiqa qo'shish
        dt = datetime.combine(date, current_time)
        dt += timedelta(minutes=15)
        current_time = dt.time()

    return available_slots


# ============= STATISTICS HELPERS =============

def get_dashboard_stats():
    """
    ✅ Dashboard statistikasini olish
    """
    from .models import Department, Service, Doctor, Appointment, ContactMessage
    from django.db.models import Count, Q
    from datetime import timedelta

    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    stats = {
        'total_departments': Department.objects.filter(is_active=True).count(),
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_doctors': Doctor.objects.filter(is_active=True).count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'today_appointments': Appointment.objects.filter(date=today).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'monthly_appointments': Appointment.objects.filter(
            created_at__gte=last_30_days
        ).count(),
        'monthly_services_views': Service.objects.filter(
            is_active=True
        ).aggregate(total_views=Sum('view_count'))['total_views'] or 0,
    }

    return stats


# ============= EXPORT HELPERS =============

import csv
from django.http import HttpResponse


def export_to_csv(queryset, filename, fields):
    """
    ✅ QuerySet ni CSV ga export qilish
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)

    # Header
    writer.writerow(fields)

    # Data
    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)

    return response