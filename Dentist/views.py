"""
DentCare Stomatologiya Klinikasi - Views
=========================================
Barcha view funksiyalari
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from collections import defaultdict
import requests
import os
from .forms import TestimonialForm
from dotenv import load_dotenv

from config import settings
from .models import (Department, Doctor, Service, Appointment, Testimonial, GalleryImage, FAQ, SiteSettings, About, WorkingHours, DoctorLeave)
from .forms import AppointmentForm, ContactForm

load_dotenv()
# ============================================================================
# ASOSIY SAHIFALAR
# ============================================================================

@cache_page(60 * 5)  # 5 daqiqa cache
def index(request):
    """Bosh sahifa"""

    # Bosh shifokor
    chief_doctor = Doctor.objects.filter(is_available=True).only('first_name', 'last_name', 'photo', 'phone').order_by('order', 'id').first()

    # Bo'limlar
    departments = Department.objects.filter(is_active=True).only('id', 'name', 'slug', 'icon', 'description', 'image')[:6]

    # Mashhur xizmatlar
    popular_services = Service.objects.filter(is_active=True, is_popular=True).select_related('department').only(
        'id', 'name', 'slug', 'icon', 'short_description',
        'price_from', 'price_to', 'department__name', 'department__slug')[:6]

    # Featured shifokorlar
    featured_doctors = Doctor.objects.filter(is_featured=True, is_available=True).select_related('department').only(
        'id', 'first_name', 'last_name', 'slug', 'specialization',
        'photo', 'rating', 'experience_years', 'department__name')[:4]

    # Testimonials
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True).only('name', 'position', 'photo', 'rating', 'comment')[:6]

    # Galereya
    gallery_photos = GalleryImage.objects.filter(is_active=True).order_by('-created_at')[:3]

    # Mutaxassisliklar
    specialties = Doctor.objects.values_list('specialization', flat=True).distinct()

    # Statistika
    stats = {
        'total_doctors': Doctor.objects.filter(is_available=True).count(),
        'total_departments': Department.objects.filter(is_active=True).count(),
        'total_services': Service.objects.filter(is_active=True).count(),
        'total_appointments': Appointment.objects.filter(
            status='completed'
        ).count() or 15000,
    }

    context = {
        'chief_doctor': chief_doctor,
        'departments': departments,
        'popular_services': popular_services,
        'featured_doctors': featured_doctors,
        'testimonials': testimonials,
        'stats': stats,
        'gallery_photos': gallery_photos,
        'specialties': specialties,
    }

    return render(request, 'index.html', context)


def about(request):
    """Biz haqimizda"""

    about_data = About.objects.first()

    departments = Department.objects.filter(
        is_active=True
    ).order_by('order')

    # Klinika rasmlari
    clinic_images = GalleryImage.objects.filter(
        category='clinic',
        is_active=True
    ).order_by('order')[:3]

    # Statistika
    stats = {
        'doctors_count': Doctor.objects.filter(is_available=True).count(),
        'departments_count': departments.count(),
        'experience_sum': Doctor.objects.aggregate(
            Sum('experience_years')
        )['experience_years__sum'] or 0,
        'patients_total': Doctor.objects.aggregate(
            Sum('patients_count')
        )['patients_count__sum'] or 0,
    }

    context = {
        'about_data': about_data,
        'departments': departments,
        'clinic_images': clinic_images,
        'stats': stats,
    }

    return render(request, 'about.html', context)


# ============================================================================
# BO'LIMLAR (DEPARTMENTS)
# ============================================================================

def departments(request):
    """Bo'limlar ro'yxati"""

    departments_list = Department.objects.filter(
        is_active=True
    ).annotate(
        doctor_count=Count('doctors', filter=Q(doctors__is_available=True)),
        service_count=Count('services', filter=Q(services__is_active=True))
    ).only(
        'id', 'name', 'slug', 'icon', 'description', 'image'
    )

    context = {
        'departments': departments_list,
    }

    return render(request, 'departments.html', context)


def department_detail(request, slug):
    """Bo'lim tafsilotlari"""

    department = get_object_or_404(
        Department.objects.select_related(),
        slug=slug,
        is_active=True
    )

    # Bo'lim shifokorlari
    doctors = Doctor.objects.filter(
        department=department,
        is_available=True
    ).only(
        'id', 'first_name', 'last_name', 'slug',
        'specialization', 'photo', 'rating'
    )

    # Bo'lim xizmatlari
    services = Service.objects.filter(
        department=department,
        is_active=True
    ).only(
        'id', 'name', 'slug', 'icon', 'short_description',
        'price_from', 'duration'
    )

    working_hours = WorkingHours.objects.all().order_by('day')

    context = {
        'department': department,
        'doctors': doctors,
        'services': services,
        'working_hours': working_hours,  # Yangi!
    }

    return render(request, 'department-details.html', context)


# ============================================================================
# XIZMATLAR (SERVICES)
# ============================================================================

def services(request):
    """Xizmatlar ro'yxati"""

    services_list = Service.objects.filter(
        is_active=True
    ).select_related('department').only(
        'id', 'name', 'slug', 'icon', 'short_description',
        'price_from', 'duration', 'is_popular',
        'department__name', 'department__slug'
    )

    context = {
        'services': services_list,
    }

    return render(request, 'services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)

    # O'xshash xizmatlar (same department)
    related_services = Service.objects.filter(
        department=service.department,
        is_active=True
    ).exclude(id=service.id).only(
        'id', 'name', 'slug', 'icon', 'short_description',
        'price_from', 'duration'
    )[:3]

    # Ish vaqti
    working_hours = WorkingHours.objects.filter(
        is_working_day=True
    ).order_by('day')[:3]

    # FAQ (xizmat yoki umumiy)
    faqs = FAQ.objects.filter(
        is_active=True,
        category='treatment'  # yoki service bilan bog'liq
    ).order_by('order')[:5]

    context = {
        'service': service,
        'related_services': related_services,
        'working_hours': working_hours,
        'faqs': faqs,
    }

    return render(request, 'service-details.html', context)
# ============================================================================
# SHIFOKORLAR (DOCTORS)
# ============================================================================

def doctors(request):
    """
    Shifokorlar ro'yxati — GET params:
      - doctor_name: qidiruv (ism yoki kalit so'z)
      - location: department id (string) yoki department slug
      - specialty: mutaxassislik nomi (string)
    Context (template uchun):
      - doctors, departments, specialties, featured_doctor,
        total_experience, total_patients
    """
    # Asosiy queryset
    doctors_qs = Doctor.objects.filter(is_available=True).select_related('department')

    # Qidiruv (ism yoki kalit so'z)
    name_q = request.GET.get('doctor_name', '').strip()
    if name_q:
        doctors_qs = doctors_qs.filter(
            Q(first_name__icontains=name_q) |
            Q(last_name__icontains=name_q) |
            Q(specialization__icontains=name_q) |
            Q(bio__icontains=name_q)
        )

    # Bo'lim (location) - template’da biz dept.id yuboryapmiz,
    # lekin foydalanuvchi slug ham yuborishi mumkin — ikkisini ham qo'llab-quvvatlaymiz.
    # request.GET dan olish
    location = request.GET.get('department', '').strip()
    department_obj = None
    if location:
        # agar id yuborilsa
        try:
            department_obj = Department.objects.get(id=int(location))
        except (ValueError, Department.DoesNotExist):
            # yoki slug bo'lsa
            department_obj = Department.objects.filter(slug=location).first()

    if department_obj:
        doctors_qs = doctors_qs.filter(department=department_obj)
    # Mutaxassislik filtri
    specialty = request.GET.get('specialty', '').strip()
    if specialty:
        doctors_qs = doctors_qs.filter(specialization__iexact=specialty)

    # Tartiblash (masalan feature/ordering)
    doctors_qs = doctors_qs.order_by('order', 'last_name')

    # Qo'shimcha context ma'lumotlari
    departments = Department.objects.filter(is_active=True).annotate(
        doctor_count=Count('doctors', filter=Q(doctors__is_available=True))
    ).order_by('order', 'name')

    specialties = Doctor.objects.values_list('specialization', flat=True).distinct()

    featured_doctor = Doctor.objects.filter(is_featured=True, is_available=True).first()

    # Statistika (misol uchun jami yillik tajriba va bemorlar soni)
    total_experience = doctors_qs.aggregate(total=Sum('experience_years'))['total'] or 0
    total_patients = doctors_qs.aggregate(total=Sum('patients_count'))['total'] or 0

    context = {
        'doctors': doctors_qs,
        'departments': departments,
        'specialties': specialties,
        'featured_doctor': featured_doctor,
        'total_experience': total_experience,
        'total_patients': total_patients,
    }

    return render(request, 'doctors.html', context)

def doctor_detail(request, slug):
    """
    Shifokor profili sahifasi
    URL: /doctors/<slug>/
    Context:
      - doctor: Doctor obyekti
      - related_doctors: shu bo'limdagi boshqa shifokorlar (sidebar)
      - working_hours: klinika umumiy ish vaqtlari
      - testimonials: aktiv bemorlar fikrlari (so'nggi 6 ta)
    """
    doctor = get_object_or_404(
        Doctor.objects.select_related('department'),
        slug=slug
    )

    # Shu bo'limdagi boshqa shifokorlar
    related_doctors = Doctor.objects.filter(
        department=doctor.department,
        is_available=True
    ).exclude(id=doctor.id).only(
        'id', 'first_name', 'last_name', 'slug', 'photo', 'specialization'
    )[:6]

    # Klinika umumiy ish vaqtlari (agar mavjud bo'lsa)
    working_hours = WorkingHours.objects.filter(is_working_day=True).order_by('day')

    # Bemorlar fikrlari (faqat faol)
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:6]

    # Bo'lim xizmatlari (faqat faol)
    department_services = doctor.department.services.filter(is_active=True).only(
        'id', 'name', 'slug', 'short_description', 'price_from', 'duration'
    )

    context = {
        'doctor': doctor,
        'related_doctors': related_doctors,
        'working_hours': working_hours,
        'testimonials': testimonials,
        'department_services': department_services,
    }
    return render(request, 'doctor-detail.html', context)


# ============================================================================
# QABULGA YOZILISH (APPOINTMENT)
# ============================================================================

def send_telegram_message(message):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload, timeout=5)
        # Terminalda tekshirish uchun:
        print(f"Telegram status code: {response.status_code}")
        print(f"Telegram response: {response.text}")

        return response.status_code == 200
    except Exception as e:
        print(f"Telegram ulanish xatosi: {e}")
        return False

@require_http_methods(["GET", "POST"])
def appointment(request):
    """Qabulga yozilish - Tuzatilgan variant"""

    if request.method == 'POST':
        form = AppointmentForm(request.POST)

        if form.is_valid():
            # 1. Ma'lumotni bazaga saqlaymiz (Telegramdan qat'i nazar)
            appointment_obj = form.save()

            # 2. Telegram xabari matnini tayyorlaymiz
            message = (
                f"🦷 <b>Yangi qabul!</b>\n\n"
                f"👤 {appointment_obj.name}\n"
                f"📞 {appointment_obj.phone}\n"
                f"📅 {appointment_obj.appointment_date}\n"
                f"📅 {appointment_obj.appointment_time}\n"
                f"🏥 {appointment_obj.department.name}"
            )
            if appointment_obj.doctor:
                message += f"\n👨‍⚕️ {appointment_obj.doctor.get_full_name()}"

            # 3. Telegramga yuborishni sinab ko'ramiz
            send_telegram_message(message)

            # 4. Foydalanuvchiga har doim muvaffaqiyat xabarini ko'rsatamiz
            messages.success(
                request,
                f"Hurmatli {appointment_obj.name}, qabulga muvaffaqiyatli yozildingiz! "
                f"Tez orada {appointment_obj.phone} raqamiga qo'ng'iroq qilamiz."
            )
            return redirect('appointment')

        else:
            # Forma xato to'ldirilgan bo'lsa
            messages.error(request, "Formada xatolik bor, iltimos ma'lumotlarni tekshiring.")

    else:
        form = AppointmentForm()

    # Bo'limlar va shifokorlar ro'yxati (GET va POST xatolari uchun)
    departments_list = Department.objects.filter(is_active=True).only('id', 'name')
    doctors_list = Doctor.objects.filter(is_available=True).select_related('department')

    context = {
        'form': form,
        'departments': departments_list,
        'doctors': doctors_list,
        'today': date.today(),
    }

    # Bu return har doim ishlashi shart!
    return render(request, 'appointment.html', context)

# ============================================================================
# AJAX FUNKSIYALAR
# ============================================================================

def load_doctors(request):
    """Bo'lim bo'yicha shifokorlarni yuklash (AJAX)"""

    department_id = request.GET.get('department_id')

    doctors = Doctor.objects.filter(
        department_id=department_id,
        is_available=True
    ).order_by('first_name')

    doctor_list = [
        {
            "id": d.id,
            "name": f"Dr. {d.first_name} {d.last_name}"
        }
        for d in doctors
    ]

    return JsonResponse(doctor_list, safe=False)


def get_available_times(request):
    """Shifokor va sana bo'yicha bo'sh vaqtlarni olish (AJAX)"""

    doctor_id = request.GET.get('doctor_id')
    date_str = request.GET.get('date')

    if not (doctor_id and date_str):
        return JsonResponse({'available_slots': []})

    doctor = get_object_or_404(Doctor, id=doctor_id)
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Shifokor bu kuni ishlaydimi?
    days = ['is_mon', 'is_tue', 'is_wed', 'is_thu', 'is_fri', 'is_sat', 'is_sun']
    weekday_field = days[date_obj.weekday()]

    if not getattr(doctor, weekday_field):
        return JsonResponse(
            {'error': 'Shifokor bu kuni ishlamaydi'},
            status=400
        )

    # Dam olishdami?
    if DoctorLeave.objects.filter(doctor=doctor, date=date_obj).exists():
        return JsonResponse(
            {'error': 'Shifokor bu kuni dam olishda'},
            status=400
        )

    # Bo'sh vaqtlarni generatsiya qilish
    available_slots = []
    current_time = datetime.combine(date_obj, doctor.work_start)
    end_time = datetime.combine(date_obj, doctor.work_end)
    interval = timedelta(minutes=doctor.consultation_duration)

    # Band vaqtlar
    booked_times = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=date_obj,
        status__in=['pending', 'confirmed']
    ).values_list('appointment_time', flat=True)

    while current_time + interval <= end_time:
        slot_time = current_time.time()
        if slot_time not in booked_times:
            available_slots.append(slot_time.strftime('%H:%M'))
        current_time += interval

    return JsonResponse({'available_slots': available_slots})


# ============================================================================
# BOSHQA SAHIFALAR
# ============================================================================

def testimonials(request):
    """Bemorlar fikri"""

    testimonials_list = Testimonial.objects.filter(
        is_active=True
    ).only(
        'name', 'position', 'photo', 'rating', 'comment'
    )

    context = {
        'testimonials': testimonials_list,
    }

    return render(request, 'testimonials.html', context)


def gallery(request):
    """Galereya"""

    category = request.GET.get('category', None)

    images = GalleryImage.objects.filter(is_active=True)

    if category:
        images = images.filter(category=category)

    images = images.only('id', 'title', 'description', 'image', 'category')

    context = {
        'images': images,
        'selected_category': category,
    }

    return render(request, 'gallery.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            message = (
                f"📩 <b>Yangi xabar (Bog'lanish)</b>\n\n"
                f"👤 Ism: {contact_message.name}\n"
                f"📞 Tel: {contact_message.phone}\n"
                f"📝 Mavzu: {contact_message.subject}\n"
                f"💬 Xabar: {contact_message.message}"
            )

            send_telegram_message(message)  #

            messages.success(request, f"Rahmat, {contact_message.name}! Xabaringiz qabul qilindi.")
            return redirect('contact')
        else:
            # Xatoni terminalda ko'rish uchun
            print(form.errors)
            messages.error(request, "Iltimos, ma'lumotlarni to'g'ri kiriting.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def testimonials(request):
    """Bemorlar fikrlari ko'rsatish va yangi fikr qoldirish"""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            t = form.save(commit=False)
            t.is_active = False  # admin tasdig'iga qoldirish yaxshidir
            t.save()
            messages.success(request, "Fikringiz qabul qilindi — tez orada e'lon qilinadi.")
            return redirect('testimonials')
        else:
            messages.error(request, "Formada xatolik bor, iltimos qayta urinib ko'ring.")
    else:
        form = TestimonialForm()

    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'testimonials': testimonials,
        'form': form,
    }
    return render(request, 'testimonials.html', context)


def faq(request):
    """Savol-Javoblar"""

    faqs = FAQ.objects.filter(
        is_active=True
    ).only('id', 'question', 'answer', 'category')

    # Category bo'yicha guruhlash
    categories = defaultdict(list)
    for faq_item in faqs:
        category_name = faq_item.get_category_display()
        categories[category_name].append(faq_item)

    context = {
        'categories': dict(categories),
    }

    return render(request, 'faq.html', context)


def terms(request):
    """Foydalanish shartlari"""
    return render(request, 'terms.html')


def privacy(request):
    """Maxfiylik siyosati"""
    return render(request, 'privacy.html')


# ============================================================================
# XATO SAHIFALAR
# ============================================================================

def custom_404(request, exception=None):
    """404 - Sahifa topilmadi"""
    return render(request, '404.html', status=404)


def custom_500(request):
    """500 - Server xatosi"""
    return render(request, '500.html', status=500)