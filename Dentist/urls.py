"""
DentCare Stomatologiya Klinikasi - URLs
========================================
SEO-friendly va toza URL tuzilmasi
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


# ============================================================================
# MAIN URL PATTERNS
# ============================================================================

urlpatterns = [
    # Asosiy sahifalar
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # Bo'limlar
    path('departments/', views.departments, name='departments'),
    path('departments/<slug:slug>/', views.department_detail, name='department_detail'),

    # Xizmatlar
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),

    # Shifokorlar
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/<slug:slug>/', views.doctor_detail, name='doctor_detail'),

    # Qabulga yozilish
    path('appointment/', views.appointment, name='appointment'),

    # Boshqa sahifalar
    path('testimonials/', views.testimonials, name='testimonials'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),

    # Statik sahifalar
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),

    # AJAX endpoints
    path('ajax/load-doctors/', views.load_doctors, name='ajax_load_doctors'),
    # urls.py ichida
    path('ajax/get-available-times/', views.get_available_times, name='get_available_times'),]


# ============================================================================
# MEDIA VA STATIC FILES (faqat development uchun)
# ============================================================================

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# ============================================================================
# CUSTOM ERROR HANDLERS (settings.py da qo'shish kerak)
# ============================================================================

# handler404 = 'Dentist.views.custom_404'
# handler500 = 'Dentist.views.custom_500'