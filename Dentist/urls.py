from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # Departments
    path('departments/', views.departments, name='departments'),
    path('department/<int:pk>/', views.department_detail, name='department-detail'),

    # Services
    path('services/', views.services_list, name='services'),
    path('service/<int:pk>/', views.service_detail, name='service-detail'),

    # Doctors
    path('doctors/', views.doctors_list, name='doctors'),

    # Other pages
    path('testimonials/', views.testimonials_list, name='testimonials'),
    path('gallery/', views.gallery_list, name='gallery'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('faq/', views.faq_list, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),

    # Language
    path('set-language/', views.set_language, name='set_language'),
]