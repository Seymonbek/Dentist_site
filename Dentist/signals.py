# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
# from django.utils.text import slugify
#
#
# class Department(models.Model):
#     """Stomatologiya bo'limlari (Departments)"""
#     name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
#     name_ru = models.CharField(max_length=200, verbose_name="Название (RU)")
#     name_en = models.CharField(max_length=200, verbose_name="Name (EN)")
#
#     description_uz = models.TextField(verbose_name="Tavsif (UZ)")
#     description_ru = models.TextField(verbose_name="Описание (RU)")
#     description_en = models.TextField(verbose_name="Description (EN)")
#
#     slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name="Slug")
#     icon = models.CharField(max_length=50, default="bi bi-activity", verbose_name="Bootstrap Icon")
#     image = models.ImageField(upload_to='departments/', blank=True, null=True, verbose_name="Rasm")
#
#     order = models.IntegerField(default=0, verbose_name="Tartib", db_index=True)
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
#
#     class Meta:
#         verbose_name = "Bo'lim"
#         verbose_name_plural = "Bo'limlar"
#         ordering = ['order', '-created_at']
#         indexes = [
#             models.Index(fields=['is_active', 'order']),
#         ]
#
#     def __str__(self):
#         return self.name_uz
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name_en) or slugify(self.name_uz)
#         super().save(*args, **kwargs)
#
#     @property
#     def active_services_count(self):
#         return self.services.filter(is_active=True).count()
#
#     @property
#     def active_doctors_count(self):
#         return self.doctors.filter(is_active=True).count()
#
#
# class Service(models.Model):
#     """Stomatologiya xizmatlari (Services)"""
#     department = models.ForeignKey(
#         Department,
#         on_delete=models.CASCADE,
#         related_name='services',
#         verbose_name="Bo'lim"
#     )
#
#     name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
#     name_ru = models.CharField(max_length=200, verbose_name="Название (RU)")
#     name_en = models.CharField(max_length=200, verbose_name="Name (EN)")
#
#     short_description_uz = models.TextField(max_length=300, verbose_name="Qisqa tavsif (UZ)")
#     short_description_ru = models.TextField(max_length=300, verbose_name="Краткое описание (RU)")
#     short_description_en = models.TextField(max_length=300, verbose_name="Short description (EN)")
#
#     description_uz = models.TextField(verbose_name="To'liq tavsif (UZ)")
#     description_ru = models.TextField(verbose_name="Полное описание (RU)")
#     description_en = models.TextField(verbose_name="Full description (EN)")
#
#     price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         blank=True,
#         null=True,
#         verbose_name="Narx",
#         validators=[MinValueValidator(0)]
#     )
#     duration = models.IntegerField(
#         blank=True,
#         null=True,
#         verbose_name="Davomiyligi (daqiqa)",
#         validators=[MinValueValidator(1), MaxValueValidator(480)]
#     )
#
#     slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name="Slug")
#     icon = models.CharField(max_length=50, default="bi bi-check-circle", verbose_name="Bootstrap Icon")
#     image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Rasm")
#
#     order = models.IntegerField(default=0, verbose_name="Tartib", db_index=True)
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#     is_featured = models.BooleanField(default=False, verbose_name="Asosiy sahifada ko'rsatish")
#
#     view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
#
#     class Meta:
#         verbose_name = "Xizmat"
#         verbose_name_plural = "Xizmatlar"
#         ordering = ['order', '-created_at']
#         indexes = [
#             models.Index(fields=['department', 'is_active']),
#             models.Index(fields=['is_featured', 'is_active']),
#         ]
#
#     def __str__(self):
#         return self.name_uz
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name_en) or slugify(self.name_uz)
#         super().save(*args, **kwargs)
#
#     def increment_view_count(self):
#         self.view_count += 1
#         self.save(update_fields=['view_count'])
#
#
# class Doctor(models.Model):
#     """Shifokorlar (Doctors)"""
#     first_name = models.CharField(max_length=100, verbose_name="Ism")
#     last_name = models.CharField(max_length=100, verbose_name="Familiya")
#
#     specialty_uz = models.CharField(max_length=200, verbose_name="Mutaxassislik (UZ)")
#     specialty_ru = models.CharField(max_length=200, verbose_name="Специальность (RU)")
#     specialty_en = models.CharField(max_length=200, verbose_name="Specialty (EN)")
#
#     bio_uz = models.TextField(verbose_name="Biografiya (UZ)")
#     bio_ru = models.TextField(verbose_name="Биография (RU)")
#     bio_en = models.TextField(verbose_name="Biography (EN)")
#
#     experience_years = models.IntegerField(
#         verbose_name="Tajriba (yil)",
#         validators=[MinValueValidator(0), MaxValueValidator(60)]
#     )
#     education_uz = models.TextField(verbose_name="Ta'lim (UZ)")
#     education_ru = models.TextField(verbose_name="Образование (RU)")
#     education_en = models.TextField(verbose_name="Education (EN)")
#
#     photo = models.ImageField(upload_to='doctors/', verbose_name="Foto")
#     departments = models.ManyToManyField(
#         Department,
#         related_name='doctors',
#         verbose_name="Bo'limlar"
#     )
#
#     phone_regex = RegexValidator(
#         regex=r'^\+998\d{9}$',
#         message="Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak"
#     )
#     phone = models.CharField(
#         max_length=20,
#         blank=True,
#         verbose_name="Telefon",
#         validators=[phone_regex]
#     )
#     email = models.EmailField(blank=True, verbose_name="Email")
#
#     facebook = models.URLField(blank=True, verbose_name="Facebook")
#     instagram = models.URLField(blank=True, verbose_name="Instagram")
#     twitter = models.URLField(blank=True, verbose_name="Twitter")
#     linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
#
#     slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name="Slug")
#     order = models.IntegerField(default=0, verbose_name="Tartib", db_index=True)
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#     is_featured = models.BooleanField(default=False, verbose_name="Asosiy sahifada ko'rsatish")
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
#
#     class Meta:
#         verbose_name = "Shifokor"
#         verbose_name_plural = "Shifokorlar"
#         ordering = ['order', 'last_name', 'first_name']
#         indexes = [
#             models.Index(fields=['is_active', 'order']),
#         ]
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"
#
#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}"
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(f"{self.first_name}-{self.last_name}")
#         super().save(*args, **kwargs)
#
#
# class Testimonial(models.Model):
#     """Mijozlar fikrlari (Testimonials)"""
#     name = models.CharField(max_length=100, verbose_name="Ism")
#     position_uz = models.CharField(max_length=100, blank=True, verbose_name="Lavozim/Kasb (UZ)")
#     position_ru = models.CharField(max_length=100, blank=True, verbose_name="Должность (RU)")
#     position_en = models.CharField(max_length=100, blank=True, verbose_name="Position (EN)")
#
#     text_uz = models.TextField(verbose_name="Fikr (UZ)")
#     text_ru = models.TextField(verbose_name="Отзыв (RU)")
#     text_en = models.TextField(verbose_name="Review (EN)")
#
#     photo = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Foto")
#     rating = models.IntegerField(
#         default=5,
#         choices=[(i, i) for i in range(1, 6)],
#         verbose_name="Reyting",
#         validators=[MinValueValidator(1), MaxValueValidator(5)]
#     )
#
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#     is_featured = models.BooleanField(default=False, verbose_name="Asosiy sahifada ko'rsatish")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#
#     class Meta:
#         verbose_name = "Fikr"
#         verbose_name_plural = "Mijozlar fikrlari"
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.name} - {self.rating}⭐"
#
#
# class Gallery(models.Model):
#     """Galereya (Gallery)"""
#     CATEGORY_CHOICES = [
#         ('clinic', 'Klinika'),
#         ('equipment', 'Jihozlar'),
#         ('team', 'Jamoa'),
#         ('patients', 'Bemorlar'),
#         ('other', 'Boshqa'),
#     ]
#
#     title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (UZ)")
#     title_ru = models.CharField(max_length=200, verbose_name="Заголовок (RU)")
#     title_en = models.CharField(max_length=200, verbose_name="Title (EN)")
#
#     category = models.CharField(
#         max_length=20,
#         choices=CATEGORY_CHOICES,
#         default='other',
#         verbose_name="Kategoriya",
#         db_index=True
#     )
#     image = models.ImageField(upload_to='gallery/', verbose_name="Rasm")
#
#     order = models.IntegerField(default=0, verbose_name="Tartib", db_index=True)
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#
#     class Meta:
#         verbose_name = "Galereya rasmi"
#         verbose_name_plural = "Galereya"
#         ordering = ['order', '-created_at']
#         indexes = [
#             models.Index(fields=['category', 'is_active']),
#         ]
#
#     def __str__(self):
#         return self.title_uz
#
#
# class Appointment(models.Model):
#     """Qabulga yozilish (Appointments)"""
#     STATUS_CHOICES = [
#         ('pending', 'Kutilmoqda'),
#         ('confirmed', 'Tasdiqlangan'),
#         ('completed', 'Yakunlangan'),
#         ('cancelled', 'Bekor qilingan'),
#     ]
#
#     name = models.CharField(max_length=100, verbose_name="Ism Familiya")
#
#     phone_regex = RegexValidator(
#         regex=r'^\+998\d{9}$',
#         message="Telefon raqami +998XXXXXXXXX formatida bo'lishi kerak"
#     )
#     phone = models.CharField(
#         max_length=20,
#         verbose_name="Telefon",
#         validators=[phone_regex]
#     )
#     email = models.EmailField(verbose_name="Email")
#
#     department = models.ForeignKey(
#         Department,
#         on_delete=models.SET_NULL,
#         null=True,
#         verbose_name="Bo'lim"
#     )
#     doctor = models.ForeignKey(
#         Doctor,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name="Shifokor"
#     )
#     service = models.ForeignKey(
#         Service,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         verbose_name="Xizmat"
#     )
#
#     date = models.DateField(verbose_name="Sana", db_index=True)
#     time = models.TimeField(verbose_name="Vaqt")
#     message = models.TextField(blank=True, verbose_name="Xabar")
#
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='pending',
#         verbose_name="Holat",
#         db_index=True
#     )
#     admin_notes = models.TextField(blank=True, verbose_name="Admin izohlar")
#
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
#
#     class Meta:
#         verbose_name = "Qabul"
#         verbose_name_plural = "Qabulga yozilishlar"
#         ordering = ['-date', '-time']
#         indexes = [
#             models.Index(fields=['date', 'status']),
#             models.Index(fields=['status', '-created_at']),
#         ]
#
#     def __str__(self):
#         return f"{self.name} - {self.date} {self.time}"
#
#     @property
#     def is_past(self):
#         from django.utils import timezone
#         from datetime import datetime, time as dt_time
#         now = timezone.now()
#         appointment_datetime = timezone.make_aware(
#             datetime.combine(self.date, self.time)
#         )
#         return appointment_datetime < now
#
#
# class FAQ(models.Model):
#     """Tez-tez beriladigan savollar"""
#     question_uz = models.CharField(max_length=500, verbose_name="Savol (UZ)")
#     question_ru = models.CharField(max_length=500, verbose_name="Вопрос (RU)")
#     question_en = models.CharField(max_length=500, verbose_name="Question (EN)")
#
#     answer_uz = models.TextField(verbose_name="Javob (UZ)")
#     answer_ru = models.TextField(verbose_name="Ответ (RU)")
#     answer_en = models.TextField(verbose_name="Answer (EN)")
#
#     order = models.IntegerField(default=0, verbose_name="Tartib", db_index=True)
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
#
#     class Meta:
#         verbose_name = "Savol"
#         verbose_name_plural = "FAQ"
#         ordering = ['order', '-created_at']
#
#     def __str__(self):
#         return self.question_uz
#
#
# class ContactMessage(models.Model):
#     """Kontakt xabarlari"""
#     name = models.CharField(max_length=100, verbose_name="Ism")
#     email = models.EmailField(verbose_name="Email")
#     subject = models.CharField(max_length=200, verbose_name="Mavzu")
#     message = models.TextField(verbose_name="Xabar")
#
#     is_read = models.BooleanField(default=False, verbose_name="O'qilgan", db_index=True)
#     is_replied = models.BooleanField(default=False, verbose_name="Javob berilgan")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan")
#
#     class Meta:
#         verbose_name = "Xabar"
#         verbose_name_plural = "Kontakt xabarlari"
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['is_read', '-created_at']),
#         ]
#
#     def __str__(self):
#         return f"{self.name} - {self.subject}"
#
#
# class SiteSettings(models.Model):
#     """Sayt sozlamalari"""
#     site_name_uz = models.CharField(max_length=200, default="DentaCare", verbose_name="Sayt nomi (UZ)")
#     site_name_ru = models.CharField(max_length=200, default="DentaCare", verbose_name="Название сайта (RU)")
#     site_name_en = models.CharField(max_length=200, default="DentaCare", verbose_name="Site name (EN)")
#
#     tagline_uz = models.CharField(max_length=200, verbose_name="Slogan (UZ)")
#     tagline_ru = models.CharField(max_length=200, verbose_name="Слоган (RU)")
#     tagline_en = models.CharField(max_length=200, verbose_name="Tagline (EN)")
#
#     about_uz = models.TextField(verbose_name="Biz haqimizda (UZ)")
#     about_ru = models.TextField(verbose_name="О нас (RU)")
#     about_en = models.TextField(verbose_name="About us (EN)")
#
#     address_uz = models.CharField(max_length=300, verbose_name="Manzil (UZ)")
#     address_ru = models.CharField(max_length=300, verbose_name="Адрес (RU)")
#     address_en = models.CharField(max_length=300, verbose_name="Address (EN)")
#
#     phone_1 = models.CharField(max_length=20, verbose_name="Telefon 1")
#     phone_2 = models.CharField(max_length=20, blank=True, verbose_name="Telefon 2")
#     email = models.EmailField(verbose_name="Email")
#
#     working_hours_uz = models.CharField(max_length=200, verbose_name="Ish vaqti (UZ)")
#     working_hours_ru = models.CharField(max_length=200, verbose_name="Время работы (RU)")
#     working_hours_en = models.CharField(max_length=200, verbose_name="Working hours (EN)")
#
#     facebook = models.URLField(blank=True, verbose_name="Facebook")
#     instagram = models.URLField(blank=True, verbose_name="Instagram")
#     twitter = models.URLField(blank=True, verbose_name="Twitter")
#     linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
#     youtube = models.URLField(blank=True, verbose_name="YouTube")
#
#     google_maps_embed = models.TextField(blank=True, verbose_name="Google Maps iframe kodi")
#
#     logo = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="Logo")
#     favicon = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="Favicon")
#
#     meta_description_uz = models.TextField(max_length=160, blank=True, verbose_name="Meta tavsif (UZ)")
#     meta_description_ru = models.TextField(max_length=160, blank=True, verbose_name="Meta описание (RU)")
#     meta_description_en = models.TextField(max_length=160, blank=True, verbose_name="Meta description (EN)")
#
#     meta_keywords_uz = models.CharField(max_length=300, blank=True, verbose_name="Meta kalit so'zlar (UZ)")
#     meta_keywords_ru = models.CharField(max_length=300, blank=True, verbose_name="Meta ключевые слова (RU)")
#     meta_keywords_en = models.CharField(max_length=300, blank=True, verbose_name="Meta keywords (EN)")
#
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan")
#
#     class Meta:
#         verbose_name = "Sayt sozlamasi"
#         verbose_name_plural = "Sayt sozlamalari"
#
#     def __str__(self):
#         return "Sayt sozlamalari"
#
#     def save(self, *args, **kwargs):
#         # Faqat bitta sozlama ob'ekti bo'lishi kerak
#         if not self.pk and SiteSettings.objects.exists():
#             return SiteSettings.objects.first()
#         return super(SiteSettings, self).save(*args, **kwargs)
#
#
# class Statistic(models.Model):
#     """Statistika (Years of experience, Happy patients, etc.)"""
#     label_uz = models.CharField(max_length=100, verbose_name="Yorliq (UZ)")
#     label_ru = models.CharField(max_length=100, verbose_name="Метка (RU)")
#     label_en = models.CharField(max_length=100, verbose_name="Label (EN)")
#
#     value = models.IntegerField(
#         verbose_name="Qiymat",
#         validators=[MinValueValidator(0)]
#     )
#     icon = models.CharField(max_length=50, default="bi bi-award", verbose_name="Bootstrap Icon")
#
#     order = models.IntegerField(default=0, verbose_name="Tartib", db_index=True)
#     is_active = models.BooleanField(default=True, verbose_name="Faol", db_index=True)
#
#     class Meta:
#         verbose_name = "Statistika"
#         verbose_name_plural = "Statistikalar"
#         ordering = ['order']
#
#     def __str__(self):
#         return f"{self.label_uz} - {self.value}"


"""
✅ FIXED: Signals for cache invalidation and file cleanup
"""

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
import os
import logging

from .models import (
    Department, Service, Doctor, SiteSettings,
    Testimonial, Gallery, FAQ, Statistic
)

logger = logging.getLogger(__name__)


# ============= CACHE INVALIDATION SIGNALS =============

@receiver([post_save, post_delete], sender=Department)
def clear_department_cache(sender, instance, **kwargs):
    """✅ Bo'lim o'zgarganda cache ni tozalash"""
    cache_keys = [
        'header_departments_v2',
        'site_settings_v2',
    ]
    for key in cache_keys:
        cache.delete(key)
    logger.info(f"Department cache cleared for: {instance}")


@receiver([post_save, post_delete], sender=Service)
def clear_service_cache(sender, instance, **kwargs):
    """✅ Xizmat o'zgarganda cache ni tozalash"""
    cache_keys = [
        'header_services_v2',
        'site_settings_v2',
    ]
    for key in cache_keys:
        cache.delete(key)
    logger.info(f"Service cache cleared for: {instance}")


@receiver(post_save, sender=SiteSettings)
def clear_site_settings_cache(sender, instance, **kwargs):
    """✅ Sayt sozlamalari o'zgarganda cache ni tozalash"""
    cache.delete('site_settings_v2')
    logger.info("Site settings cache cleared")


@receiver([post_save, post_delete], sender=Doctor)
@receiver([post_save, post_delete], sender=Testimonial)
@receiver([post_save, post_delete], sender=Gallery)
@receiver([post_save, post_delete], sender=FAQ)
@receiver([post_save, post_delete], sender=Statistic)
def clear_general_cache(sender, instance, **kwargs):
    """✅ Umumiy cache ni tozalash"""
    # View cache'larini tozalash
    cache.clear()
    logger.info(f"General cache cleared for: {sender.__name__}")


# ============= FILE CLEANUP SIGNALS =============

@receiver(pre_delete, sender=Department)
def delete_department_files(sender, instance, **kwargs):
    """✅ Bo'lim o'chirilganda rasmlarini ham o'chirish"""
    if instance.image:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
                logger.info(f"Deleted department image: {instance.image.path}")
        except Exception as e:
            logger.error(f"Error deleting department image: {str(e)}")


@receiver(pre_delete, sender=Service)
def delete_service_files(sender, instance, **kwargs):
    """✅ Xizmat o'chirilganda rasmlarini ham o'chirish"""
    if instance.image:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
                logger.info(f"Deleted service image: {instance.image.path}")
        except Exception as e:
            logger.error(f"Error deleting service image: {str(e)}")


@receiver(pre_delete, sender=Doctor)
def delete_doctor_files(sender, instance, **kwargs):
    """✅ Shifokor o'chirilganda rasmlarini ham o'chirish"""
    if instance.photo:
        try:
            if os.path.isfile(instance.photo.path):
                os.remove(instance.photo.path)
                logger.info(f"Deleted doctor photo: {instance.photo.path}")
        except Exception as e:
            logger.error(f"Error deleting doctor photo: {str(e)}")


@receiver(pre_delete, sender=Testimonial)
def delete_testimonial_files(sender, instance, **kwargs):
    """✅ Testimonial o'chirilganda rasmlarini ham o'chirish"""
    if instance.photo:
        try:
            if os.path.isfile(instance.photo.path):
                os.remove(instance.photo.path)
                logger.info(f"Deleted testimonial photo: {instance.photo.path}")
        except Exception as e:
            logger.error(f"Error deleting testimonial photo: {str(e)}")


@receiver(pre_delete, sender=Gallery)
def delete_gallery_files(sender, instance, **kwargs):
    """✅ Galereya rasmi o'chirilganda faylni ham o'chirish"""
    if instance.image:
        try:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
                logger.info(f"Deleted gallery image: {instance.image.path}")
        except Exception as e:
            logger.error(f"Error deleting gallery image: {str(e)}")


@receiver(pre_delete, sender=SiteSettings)
def delete_site_settings_files(sender, instance, **kwargs):
    """✅ Sayt sozlamalari o'chirilganda fayllarni ham o'chirish"""
    files_to_delete = []

    if instance.logo:
        files_to_delete.append(instance.logo.path)

    if instance.favicon:
        files_to_delete.append(instance.favicon.path)

    for file_path in files_to_delete:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Deleted site settings file: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting site settings file: {str(e)}")


# ============= UPDATE FILE CLEANUP =============

@receiver(post_save, sender=Department)
def clean_old_department_image(sender, instance, **kwargs):
    """✅ Yangi rasm yuklaganda eskisini o'chirish"""
    if not instance.pk:
        return

    try:
        old_instance = Department.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            if os.path.isfile(old_instance.image.path):
                os.remove(old_instance.image.path)
                logger.info(f"Cleaned old department image: {old_instance.image.path}")
    except Department.DoesNotExist:
        pass
    except Exception as e:
        logger.error(f"Error cleaning old department image: {str(e)}")


@receiver(post_save, sender=Service)
def clean_old_service_image(sender, instance, **kwargs):
    """✅ Yangi rasm yuklaganda eskisini o'chirish"""
    if not instance.pk:
        return

    try:
        old_instance = Service.objects.get(pk=instance.pk)
        if old_instance.image and old_instance.image != instance.image:
            if os.path.isfile(old_instance.image.path):
                os.remove(old_instance.image.path)
                logger.info(f"Cleaned old service image: {old_instance.image.path}")
    except Service.DoesNotExist:
        pass
    except Exception as e:
        logger.error(f"Error cleaning old service image: {str(e)}")


@receiver(post_save, sender=Doctor)
def clean_old_doctor_photo(sender, instance, **kwargs):
    """✅ Yangi rasm yuklaganda eskisini o'chirish"""
    if not instance.pk:
        return

    try:
        old_instance = Doctor.objects.get(pk=instance.pk)
        if old_instance.photo and old_instance.photo != instance.photo:
            if os.path.isfile(old_instance.photo.path):
                os.remove(old_instance.photo.path)
                logger.info(f"Cleaned old doctor photo: {old_instance.photo.path}")
    except Doctor.DoesNotExist:
        pass
    except Exception as e:
        logger.error(f"Error cleaning old doctor photo: {str(e)}")