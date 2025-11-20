# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.utils.translation import get_language, activate, gettext as _
# from django.conf import settings
# from django.db.models import Q, Count, Prefetch
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.decorators.cache import cache_page
#
#
# from .models import (
#     Department, Service, Doctor, Testimonial, Gallery,
#     FAQ, Statistic
# )
# from .forms import AppointmentForm, ContactForm
#
#
# def set_language(request):
#     """Tilni o'zgartirish"""
#     language = request.GET.get('language', 'uz')
#     if language in ['uz', 'ru', 'en']:
#         activate(language)
#         request.session[settings.LANGUAGE_COOKIE_NAME] = language
#
#     # Oldingi sahifaga qaytish
#     next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
#     return redirect(next_url)
#
#
# def get_common_context():
#     """Barcha sahifalar uchun umumiy kontekst"""
#     return {
#         'departments': Department.objects.filter(is_active=True).only(
#             'id', 'name_uz', 'name_ru', 'name_en', 'icon'
#         )[:10],
#         'services': Service.objects.filter(is_active=True).select_related('department').only(
#             'id', 'name_uz', 'name_ru', 'name_en', 'price', 'department__name_uz'
#         )[:10],
#         'statistics': Statistic.objects.filter(is_active=True),
#     }
#
#
# @cache_page(60 * 15)  # 15 daqiqa kesh
# def index(request):
#     """Asosiy sahifa"""
#     context = {
#         'departments': Department.objects.filter(is_active=True).prefetch_related('services')[:6],
#         'services': Service.objects.filter(is_active=True, is_featured=True).select_related('department')[:6],
#         'doctors': Doctor.objects.filter(is_active=True, is_featured=True).prefetch_related('departments')[:4],
#         'testimonials': Testimonial.objects.filter(is_active=True, is_featured=True)[:6],
#         'statistics': Statistic.objects.filter(is_active=True),
#         'gallery': Gallery.objects.filter(is_active=True)[:6],
#     }
#     return render(request, 'index.html', context)
#
#
# def about(request):
#     """Biz haqimizda sahifasi"""
#     context = {
#         'statistics': Statistic.objects.filter(is_active=True),
#         'doctors': Doctor.objects.filter(is_active=True).prefetch_related('departments')[:6],
#         'gallery': Gallery.objects.filter(is_active=True)[:3],
#         'departments': Department.objects.filter(is_active=True)[:6],
#     }
#     return render(request, 'about.html', context)
#
#
# def departments(request):
#     """Bo'limlar ro'yxati"""
#     departments_list = Department.objects.filter(is_active=True).annotate(
#         services_count=Count('services', filter=Q(services__is_active=True)),
#         doctors_count=Count('doctors', filter=Q(doctors__is_active=True))
#     ).prefetch_related('services')
#
#     # Pagination
#     paginator = Paginator(departments_list, 12)
#     page = request.GET.get('page')
#
#     try:
#         departments_page = paginator.page(page)
#     except PageNotAnInteger:
#         departments_page = paginator.page(1)
#     except EmptyPage:
#         departments_page = paginator.page(paginator.num_pages)
#
#     context = {
#         'departments': departments_page,
#     }
#     return render(request, 'departments.html', context)
#
#
# def department_detail(request, pk):
#     """Bo'lim tafsilotlari"""
#     department = get_object_or_404(
#         Department.objects.prefetch_related(
#             Prefetch('services', queryset=Service.objects.filter(is_active=True)),
#             Prefetch('doctors', queryset=Doctor.objects.filter(is_active=True))
#         ),
#         pk=pk,
#         is_active=True
#     )
#
#     context = {
#         'department': department,
#         'services': department.services.all(),
#         'doctors': department.doctors.all(),
#     }
#     return render(request, 'department-details.html', context)
#
#
# def services_list(request):
#     """Xizmatlar ro'yxati"""
#     department_id = request.GET.get('department')
#     search_query = request.GET.get('search', '').strip()
#
#     services = Service.objects.filter(is_active=True).select_related('department')
#
#     # Filter by department
#     if department_id:
#         services = services.filter(department_id=department_id)
#
#     # Search functionality
#     if search_query:
#         services = services.filter(
#             Q(name_uz__icontains=search_query) |
#             Q(name_ru__icontains=search_query) |
#             Q(name_en__icontains=search_query) |
#             Q(description_uz__icontains=search_query)
#         )
#
#     # Pagination
#     paginator = Paginator(services, 12)
#     page = request.GET.get('page')
#
#     try:
#         services_page = paginator.page(page)
#     except PageNotAnInteger:
#         services_page = paginator.page(1)
#     except EmptyPage:
#         services_page = paginator.page(paginator.num_pages)
#
#     context = {
#         'services': services_page,
#         'departments': Department.objects.filter(is_active=True),
#         'selected_department': department_id,
#         'search_query': search_query,
#         'statistics': Statistic.objects.filter(is_active=True),
#     }
#     return render(request, 'services.html', context)
#
#
# def service_detail(request, pk):
#     """Xizmat tafsilotlari"""
#     service = get_object_or_404(
#         Service.objects.select_related('department'),
#         pk=pk,
#         is_active=True
#     )
#
#     # Increment view count
#     service.increment_view_count()
#
#     # Related services
#     related_services = Service.objects.filter(
#         department=service.department,
#         is_active=True
#     ).exclude(pk=pk).select_related('department')[:3]
#
#     context = {
#         'service': service,
#         'related_services': related_services,
#     }
#     return render(request, 'service-details.html', context)
#
#
# def doctors_list(request):
#     """Shifokorlar ro'yxati"""
#     department_id = request.GET.get('department')
#     search_query = request.GET.get('search', '').strip()
#
#     doctors = Doctor.objects.filter(is_active=True).prefetch_related('departments')
#
#     # Filter by department
#     if department_id:
#         doctors = doctors.filter(departments__id=department_id)
#
#     # Search functionality
#     if search_query:
#         doctors = doctors.filter(
#             Q(first_name__icontains=search_query) |
#             Q(last_name__icontains=search_query) |
#             Q(specialty_uz__icontains=search_query) |
#             Q(specialty_ru__icontains=search_query) |
#             Q(specialty_en__icontains=search_query)
#         )
#
#     # Pagination
#     paginator = Paginator(doctors, 12)
#     page = request.GET.get('page')
#
#     try:
#         doctors_page = paginator.page(page)
#     except PageNotAnInteger:
#         doctors_page = paginator.page(1)
#     except EmptyPage:
#         doctors_page = paginator.page(paginator.num_pages)
#
#     context = {
#         'doctors': doctors_page,
#         'departments': Department.objects.filter(is_active=True),
#         'selected_department': department_id,
#         'search_query': search_query,
#     }
#     return render(request, 'doctors.html', context)
#
#
# def testimonials_list(request):
#     """Mijozlar fikrlari"""
#     testimonials = Testimonial.objects.filter(is_active=True)
#
#     # Pagination
#     paginator = Paginator(testimonials, 12)
#     page = request.GET.get('page')
#
#     try:
#         testimonials_page = paginator.page(page)
#     except PageNotAnInteger:
#         testimonials_page = paginator.page(1)
#     except EmptyPage:
#         testimonials_page = paginator.page(paginator.num_pages)
#
#     context = {
#         'testimonials': testimonials_page,
#     }
#     return render(request, 'testimonials.html', context)
#
#
# def gallery_list(request):
#     """Galereya"""
#     category = request.GET.get('category')
#     gallery = Gallery.objects.filter(is_active=True)
#
#     if category:
#         gallery = gallery.filter(category=category)
#
#     categories = Gallery.CATEGORY_CHOICES
#
#     # Pagination
#     paginator = Paginator(gallery, 16)
#     page = request.GET.get('page')
#
#     try:
#         gallery_page = paginator.page(page)
#     except PageNotAnInteger:
#         gallery_page = paginator.page(1)
#     except EmptyPage:
#         gallery_page = paginator.page(paginator.num_pages)
#
#     context = {
#         'gallery': gallery_page,
#         'categories': categories,
#         'selected_category': category,
#     }
#     return render(request, 'gallery.html', context)
#
#
# def appointment_view(request):
#     """Qabulga yozilish"""
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save()
#
#             # Xabar yuborish (email yoki SMS)
#             # TODO: Implement email/SMS notification
#
#             lang = get_language()
#             if lang == 'ru':
#                 success_msg = 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.'
#             elif lang == 'en':
#                 success_msg = 'Your request has been successfully submitted! We will contact you soon.'
#             else:
#                 success_msg = 'Sizning arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.'
#
#             messages.success(request, success_msg)
#             return redirect('appointment')
#         else:
#             # Form xatolarini ko'rsatish
#             lang = get_language()
#             if lang == 'ru':
#                 error_msg = 'Пожалуйста, исправьте ошибки в форме.'
#             elif lang == 'en':
#                 error_msg = 'Please correct the errors in the form.'
#             else:
#                 error_msg = 'Iltimos, formadagi xatolarni tuzating.'
#
#             messages.error(request, error_msg)
#     else:
#         form = AppointmentForm()
#
#     context = {
#         'form': form,
#         'departments': Department.objects.filter(is_active=True),
#         'doctors': Doctor.objects.filter(is_active=True).prefetch_related('departments'),
#         'services': Service.objects.filter(is_active=True).select_related('department'),
#     }
#     return render(request, 'appointment.html', context)
#
#
# @cache_page(60 * 30)  # 30 daqiqa kesh
# def faq_list(request):
#     """FAQ sahifasi"""
#     faqs = FAQ.objects.filter(is_active=True)
#
#     context = {
#         'faqs': faqs,
#     }
#     return render(request, 'faq.html', context)
#
#
# def contact(request):
#     """Kontakt sahifasi"""
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             contact_message = form.save()
#
#             # Email yuborish
#             # TODO: Implement email notification
#
#             lang = get_language()
#             if lang == 'ru':
#                 success_msg = 'Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.'
#             elif lang == 'en':
#                 success_msg = 'Your message has been successfully sent! We will respond to you soon.'
#             else:
#                 success_msg = 'Xabaringiz muvaffaqiyatli yuborildi! Tez orada javob beramiz.'
#
#             messages.success(request, success_msg)
#             return redirect('contact')
#         else:
#             lang = get_language()
#             if lang == 'ru':
#                 error_msg = 'Пожалуйста, исправьте ошибки в форме.'
#             elif lang == 'en':
#                 error_msg = 'Please correct the errors in the form.'
#             else:
#                 error_msg = 'Iltimos, formadagi xatolarni tuzating.'
#
#             messages.error(request, error_msg)
#     else:
#         form = ContactForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'contact.html', context)
#
#
# @cache_page(60 * 60)  # 1 soat kesh
# def terms(request):
#     """Foydalanish shartlari"""
#     return render(request, 'terms.html')
#
#
# @cache_page(60 * 60)  # 1 soat kesh
# def privacy(request):
#     """Maxfiylik siyosati"""
#     return render(request, 'privacy.html')
#
#
# def page_not_found(request, exception=None):
#     """404 sahifa"""
#     return render(request, '404.html', status=404)
#
#
# # API views for AJAX requests
# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
#
#
# @require_http_methods(["GET"])
# def get_doctors_by_department(request):
#     """Bo'lim bo'yicha shifokorlarni olish (AJAX)"""
#     department_id = request.GET.get('department_id')
#     if department_id:
#         doctors = Doctor.objects.filter(
#             departments__id=department_id,
#             is_active=True
#         ).values('id', 'first_name', 'last_name')
#
#         doctors_list = [
#             {
#                 'id': doctor['id'],
#                 'name': f"{doctor['first_name']} {doctor['last_name']}"
#             }
#             for doctor in doctors
#         ]
#         return JsonResponse({'doctors': doctors_list})
#
#     return JsonResponse({'doctors': []})
#
#
# @require_http_methods(["GET"])
# def get_services_by_department(request):
#     """Bo'lim bo'yicha xizmatlarni olish (AJAX)"""
#     department_id = request.GET.get('department_id')
#     lang = get_language()
#
#     if department_id:
#         services = Service.objects.filter(
#             department_id=department_id,
#             is_active=True
#         )
#
#         services_list = []
#         for service in services:
#             name = getattr(service, f'name_{lang}', service.name_uz)
#             services_list.append({
#                 'id': service.id,
#                 'name': name,
#                 'price': str(service.price) if service.price else None
#             })
#
#         return JsonResponse({'services': services_list})
#
#     return JsonResponse({'services': []})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import get_language, activate, gettext as _
from django.conf import settings
from django.db.models import Q, Count, Prefetch, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
import logging

from .models import (
    Department, Service, Doctor, Testimonial, Gallery,
    FAQ, Statistic, Appointment, ContactMessage
)
from .forms import AppointmentForm, ContactForm

# Logger sozlash
logger = logging.getLogger(__name__)


def set_language(request):
    """Tilni o'zgartirish"""
    language = request.GET.get('language', 'uz')
    if language in ['uz', 'ru', 'en']:
        activate(language)
        request.session[settings.LANGUAGE_COOKIE_NAME] = language

    # Oldingi sahifaga qaytish
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)


@cache_page(60 * 5)  # ✅ FIXED: 5 daqiqa cache
@vary_on_cookie  # ✅ FIXED: User bo'yicha farq qiladi
def index(request):
    """Asosiy sahifa"""
    try:
        context = {
            'departments': Department.objects.filter(is_active=True).prefetch_related(
                Prefetch('services', queryset=Service.objects.filter(is_active=True))
            )[:6],
            'services': Service.objects.filter(
                is_active=True,
                is_featured=True
            ).select_related('department').only(
                'id', 'name_uz', 'name_ru', 'name_en', 'slug',
                'price', 'icon', 'department__name_uz'
            )[:6],
            'doctors': Doctor.objects.filter(
                is_active=True,
                is_featured=True
            ).prefetch_related('departments').only(  # ✅ FIXED: only() qo'shildi
                'id', 'first_name', 'last_name', 'specialty_uz',
                'specialty_ru', 'specialty_en', 'photo', 'experience_years'
            )[:4],
            'testimonials': Testimonial.objects.filter(
                is_active=True,
                is_featured=True
            ).only(  # ✅ FIXED: only()
                'name', 'text_uz', 'text_ru', 'text_en',
                'position_uz', 'position_ru', 'position_en', 'rating', 'photo'
            )[:6],
            'statistics': Statistic.objects.filter(is_active=True),
            'gallery': Gallery.objects.filter(is_active=True).only(
                'title_uz', 'title_ru', 'title_en', 'image', 'category'
            )[:6],
        }
        return render(request, 'index.html', context)
    except Exception as e:  # ✅ FIXED: Error handling
        logger.error(f"Index page error: {str(e)}")
        messages.error(request, _("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."))
        return render(request, 'index.html', {'error': True})


def about(request):
    """Biz haqimizda sahifasi"""
    try:
        context = {
            'statistics': Statistic.objects.filter(is_active=True),
            'doctors': Doctor.objects.filter(is_active=True).prefetch_related('departments')[:6],
            'gallery': Gallery.objects.filter(is_active=True)[:3],
            'departments': Department.objects.filter(is_active=True)[:6],
        }
        return render(request, 'about.html', context)
    except Exception as e:  # ✅ FIXED
        logger.error(f"About page error: {str(e)}")
        messages.error(request, _("Sahifani yuklashda xatolik."))
        return redirect('index')


def departments(request):
    """Bo'limlar ro'yxati"""
    try:
        departments_list = Department.objects.filter(is_active=True).annotate(
            services_count_db=Count('services', filter=Q(services__is_active=True)),
            doctors_count_db=Count('doctors', filter=Q(doctors__is_active=True))
        ).order_by('order', '-created_at')

        # Pagination  # ✅ FIXED: Per page dynamic
        per_page = request.GET.get('per_page', 12)
        try:
            per_page = int(per_page)
            per_page = min(max(per_page, 6), 48)  # 6-48 orasida
        except (ValueError, TypeError):
            per_page = 12

        paginator = Paginator(departments_list, per_page)
        page = request.GET.get('page')

        try:
            departments_page = paginator.page(page)
        except PageNotAnInteger:
            departments_page = paginator.page(1)
        except EmptyPage:
            departments_page = paginator.page(paginator.num_pages)

        context = {
            'departments': departments_page,
        }
        return render(request, 'departments.html', context)
    except Exception as e:  # ✅ FIXED
        logger.error(f"Departments page error: {str(e)}")
        messages.error(request, _("Bo'limlarni yuklashda xatolik."))
        return redirect('index')


def department_detail(request, pk):
    """Bo'lim tafsilotlari"""
    try:
        department = get_object_or_404(
            Department.objects.prefetch_related(
                Prefetch('services', queryset=Service.objects.filter(is_active=True)),
                Prefetch('doctors', queryset=Doctor.objects.filter(is_active=True))
            ),
            pk=pk,
            is_active=True
        )

        context = {
            'department': department,
            'services': department.services.all(),
            'doctors': department.doctors.all(),
        }
        return render(request, 'department-details.html', context)
    except Department.DoesNotExist:  # ✅ FIXED: Specific exception
        messages.error(request, _("Bo'lim topilmadi"))
        raise Http404(_("Bo'lim topilmadi"))
    except Exception as e:
        logger.error(f"Department detail error: {str(e)}")
        messages.error(request, _("Sahifani yuklashda xatolik."))
        return redirect('departments')


def services_list(request):
    """Xizmatlar ro'yxati"""
    try:
        department_id = request.GET.get('department')
        search_query = request.GET.get('search', '').strip()

        services = Service.objects.filter(is_active=True).select_related('department')

        # Filter by department
        if department_id:
            try:
                department_id = int(department_id)
                services = services.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass

        # Search functionality  # ✅ FIXED: Better search
        if search_query and len(search_query) >= 2:  # Minimum 2 harf
            lang = get_language()
            services = services.filter(
                Q(**{f'name_{lang}__icontains': search_query}) |
                Q(**{f'description_{lang}__icontains': search_query})
            )

        # Pagination
        per_page = request.GET.get('per_page', 12)
        try:
            per_page = int(per_page)
            per_page = min(max(per_page, 6), 48)
        except (ValueError, TypeError):
            per_page = 12

        paginator = Paginator(services, per_page)
        page = request.GET.get('page')

        try:
            services_page = paginator.page(page)
        except PageNotAnInteger:
            services_page = paginator.page(1)
        except EmptyPage:
            services_page = paginator.page(paginator.num_pages)

        context = {
            'services': services_page,
            'departments': Department.objects.filter(is_active=True),
            'selected_department': department_id,
            'search_query': search_query,
            'statistics': Statistic.objects.filter(is_active=True),
        }
        return render(request, 'services.html', context)
    except Exception as e:
        logger.error(f"Services list error: {str(e)}")
        messages.error(request, _("Xizmatlarni yuklashda xatolik."))
        return redirect('index')


def service_detail(request, pk):
    """Xizmat tafsilotlari"""
    try:
        service = get_object_or_404(
            Service.objects.select_related('department'),
            pk=pk,
            is_active=True
        )

        # Increment view count  # ✅ FIXED: F() expression
        service.increment_view_count()

        # Related services
        related_services = Service.objects.filter(
            department=service.department,
            is_active=True
        ).exclude(pk=pk).select_related('department')[:3]

        context = {
            'service': service,
            'related_services': related_services,
        }
        return render(request, 'service-details.html', context)
    except Service.DoesNotExist:
        messages.error(request, _("Xizmat topilmadi"))
        raise Http404(_("Xizmat topilmadi"))
    except Exception as e:
        logger.error(f"Service detail error: {str(e)}")
        messages.error(request, _("Sahifani yuklashda xatolik."))
        return redirect('services')


def doctors_list(request):
    """Shifokorlar ro'yxati"""
    try:
        department_id = request.GET.get('department')
        search_query = request.GET.get('search', '').strip()

        doctors = Doctor.objects.filter(is_active=True).prefetch_related('departments')

        # Filter by department
        if department_id:
            try:
                department_id = int(department_id)
                doctors = doctors.filter(departments__id=department_id)
            except (ValueError, TypeError):
                pass

        # Search functionality
        if search_query and len(search_query) >= 2:
            doctors = doctors.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(specialty_uz__icontains=search_query) |
                Q(specialty_ru__icontains=search_query) |
                Q(specialty_en__icontains=search_query)
            )

        # Pagination
        per_page = request.GET.get('per_page', 12)
        try:
            per_page = int(per_page)
            per_page = min(max(per_page, 6), 48)
        except (ValueError, TypeError):
            per_page = 12

        paginator = Paginator(doctors, per_page)
        page = request.GET.get('page')

        try:
            doctors_page = paginator.page(page)
        except PageNotAnInteger:
            doctors_page = paginator.page(1)
        except EmptyPage:
            doctors_page = paginator.page(paginator.num_pages)

        context = {
            'doctors': doctors_page,
            'departments': Department.objects.filter(is_active=True),
            'selected_department': department_id,
            'search_query': search_query,
        }
        return render(request, 'doctors.html', context)
    except Exception as e:
        logger.error(f"Doctors list error: {str(e)}")
        messages.error(request, _("Shifokorlarni yuklashda xatolik."))
        return redirect('index')


def testimonials_list(request):
    """Mijozlar fikrlari"""
    try:
        testimonials = Testimonial.objects.filter(is_active=True)

        # Pagination
        paginator = Paginator(testimonials, 12)
        page = request.GET.get('page')

        try:
            testimonials_page = paginator.page(page)
        except PageNotAnInteger:
            testimonials_page = paginator.page(1)
        except EmptyPage:
            testimonials_page = paginator.page(paginator.num_pages)

        context = {
            'testimonials': testimonials_page,
        }
        return render(request, 'testimonials.html', context)
    except Exception as e:
        logger.error(f"Testimonials error: {str(e)}")
        messages.error(request, _("Fikrlarni yuklashda xatolik."))
        return redirect('index')


def gallery_list(request):
    """Galereya"""
    try:
        category = request.GET.get('category')
        gallery = Gallery.objects.filter(is_active=True)

        if category and category in dict(Gallery.CATEGORY_CHOICES):
            gallery = gallery.filter(category=category)

        categories = Gallery.CATEGORY_CHOICES

        # Pagination
        paginator = Paginator(gallery, 16)
        page = request.GET.get('page')

        try:
            gallery_page = paginator.page(page)
        except PageNotAnInteger:
            gallery_page = paginator.page(1)
        except EmptyPage:
            gallery_page = paginator.page(paginator.num_pages)

        context = {
            'gallery': gallery_page,
            'categories': categories,
            'selected_category': category,
        }
        return render(request, 'gallery.html', context)
    except Exception as e:
        logger.error(f"Gallery error: {str(e)}")
        messages.error(request, _("Galereyani yuklashda xatolik."))
        return redirect('index')


def appointment_view(request):
    """Qabulga yozilish"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save()

                # Xabar yuborish (email yoki SMS)
                # TODO: Implement email/SMS notification
                # send_appointment_notification(appointment)

                lang = get_language()
                success_messages = {
                    'ru': 'Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.',
                    'en': 'Your request has been successfully submitted! We will contact you soon.',
                    'uz': 'Sizning arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.'
                }

                messages.success(request, success_messages.get(lang, success_messages['uz']))
                return redirect('appointment')
            except Exception as e:  # ✅ FIXED: Error handling
                logger.error(f"Appointment creation error: {str(e)}")
                messages.error(request, _("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."))
        else:
            # Form xatolarini ko'rsatish
            lang = get_language()
            error_messages = {
                'ru': 'Пожалуйста, исправьте ошибки в форме.',
                'en': 'Please correct the errors in the form.',
                'uz': 'Iltimos, formadagi xatolarni tuzating.'
            }
            messages.error(request, error_messages.get(lang, error_messages['uz']))
    else:
        form = AppointmentForm()

    try:
        context = {
            'form': form,
            'departments': Department.objects.filter(is_active=True),
            'doctors': Doctor.objects.filter(is_active=True).prefetch_related('departments'),
            'services': Service.objects.filter(is_active=True).select_related('department'),
        }
        return render(request, 'appointment.html', context)
    except Exception as e:
        logger.error(f"Appointment page error: {str(e)}")
        messages.error(request, _("Sahifani yuklashda xatolik."))
        return redirect('index')


@cache_page(60 * 30)  # 30 daqiqa kesh
def faq_list(request):
    """FAQ sahifasi"""
    try:
        faqs = FAQ.objects.filter(is_active=True)
        context = {'faqs': faqs}
        return render(request, 'faq.html', context)
    except Exception as e:
        logger.error(f"FAQ error: {str(e)}")
        messages.error(request, _("Sahifani yuklashda xatolik."))
        return redirect('index')


def contact(request):
    """Kontakt sahifasi"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact_message = form.save()

                # Email yuborish
                # TODO: Implement email notification
                # send_contact_notification(contact_message)

                lang = get_language()
                success_messages = {
                    'ru': 'Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.',
                    'en': 'Your message has been successfully sent! We will respond to you soon.',
                    'uz': 'Xabaringiz muvaffaqiyatli yuborildi! Tez orada javob beramiz.'
                }

                messages.success(request, success_messages.get(lang, success_messages['uz']))
                return redirect('contact')
            except Exception as e:
                logger.error(f"Contact message error: {str(e)}")
                messages.error(request, _("Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."))
        else:
            lang = get_language()
            error_messages = {
                'ru': 'Пожалуйста, исправьте ошибки в форме.',
                'en': 'Please correct the errors in the form.',
                'uz': 'Iltimos, formadagi xatolarni tuzating.'
            }
            messages.error(request, error_messages.get(lang, error_messages['uz']))
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'contact.html', context)


@cache_page(60 * 60)  # 1 soat kesh
def terms(request):
    """Foydalanish shartlari"""
    return render(request, 'terms.html')


@cache_page(60 * 60)  # 1 soat kesh
def privacy(request):
    """Maxfiylik siyosati"""
    return render(request, 'privacy.html')


def page_not_found(request, exception=None):
    """404 sahifa"""
    return render(request, '404.html', status=404)


# API views for AJAX requests

@require_http_methods(["GET"])
def get_doctors_by_department(request):
    """Bo'lim bo'yicha shifokorlarni olish (AJAX)"""
    try:
        department_id = request.GET.get('department_id')
        if not department_id:
            return JsonResponse({'doctors': []})

        # ✅ FIXED: Integer validation
        try:
            department_id = int(department_id)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid department ID'}, status=400)

        doctors = Doctor.objects.filter(
            departments__id=department_id,
            is_active=True
        ).values('id', 'first_name', 'last_name')

        doctors_list = [
            {
                'id': doctor['id'],
                'name': f"{doctor['first_name']} {doctor['last_name']}"
            }
            for doctor in doctors
        ]
        return JsonResponse({'doctors': doctors_list})
    except Exception as e:
        logger.error(f"Get doctors error: {str(e)}")
        return JsonResponse({'error': 'Server error'}, status=500)


@require_http_methods(["GET"])
def get_services_by_department(request):
    """Bo'lim bo'yicha xizmatlarni olish (AJAX)"""
    try:
        department_id = request.GET.get('department_id')
        lang = get_language()

        if not department_id:
            return JsonResponse({'services': []})

        # ✅ FIXED: Integer validation
        try:
            department_id = int(department_id)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid department ID'}, status=400)

        services = Service.objects.filter(
            department_id=department_id,
            is_active=True
        ).only('id', f'name_{lang}', 'price')

        services_list = []
        for service in services:
            name = getattr(service, f'name_{lang}', service.name_uz)
            services_list.append({
                'id': service.id,
                'name': name,
                'price': float(service.price) if service.price else None
            })

        return JsonResponse({'services': services_list})
    except Exception as e:
        logger.error(f"Get services error: {str(e)}")
        return JsonResponse({'error': 'Server error'}, status=500)