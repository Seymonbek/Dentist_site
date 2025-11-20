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


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
import os


class Department(models.Model):
    """Bo'limlar modeli"""
    # O'zbek tili
    name_uz = models.CharField(_("Nomi (O'zbek)"), max_length=200)
    description_uz = models.TextField(_("Ta'rif (O'zbek)"))

    # Rus tili
    name_ru = models.CharField(_("Название (Русский)"), max_length=200)
    description_ru = models.TextField(_("Описание (Русский)"))

    # Ingliz tili
    name_en = models.CharField(_("Name (English)"), max_length=200)
    description_en = models.TextField(_("Description (English)"))

    # Qo'shimcha maydonlar
    slug = models.SlugField(max_length=200, unique=True, db_index=True)  # ✅ FIXED: unique qo'shildi
    icon = models.CharField(_("Icon class"), max_length=100, default='bi bi-hospital',
                            help_text=_("Bootstrap icon class nomi"))
    image = models.ImageField(
        _("Rasm"),
        upload_to='departments/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],  # ✅ FIXED: validator qo'shildi
        help_text=_("Ruxsat etilgan formatlar: JPG, PNG, WEBP")
    )
    order = models.IntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)  # ✅ FIXED: index qo'shildi

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("Bo'lim")
        verbose_name_plural = _("Bo'limlar")
        ordering = ['order', '-created_at']
        indexes = [  # ✅ FIXED: indexes qo'shildi
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        """✅ FIXED: Ko'p tillik qo'llab-quvvatlash"""
        from django.utils.translation import get_language
        lang = get_language()
        return getattr(self, f'name_{lang}', self.name_uz)

    def save(self, *args, **kwargs):
        """✅ FIXED: Auto slug generation"""
        if not self.slug:
            base_slug = slugify(self.name_en) or slugify(self.name_uz, allow_unicode=True)
            self.slug = base_slug

            # Unique slug yaratish
            counter = 1
            while Department.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('department-detail', kwargs={'pk': self.pk})

    @property
    def services_count(self):
        """✅ FIXED: Cached property"""
        return self.services.filter(is_active=True).count()

    @property
    def doctors_count(self):
        """✅ FIXED: Cached property"""
        return self.doctors.filter(is_active=True).count()


class Service(models.Model):
    """Xizmatlar modeli"""
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name=_("Bo'lim")
    )

    # O'zbek tili
    name_uz = models.CharField(_("Nomi (O'zbek)"), max_length=200)
    short_description_uz = models.CharField(_("Qisqa ta'rif (O'zbek)"), max_length=300)
    description_uz = models.TextField(_("To'liq ta'rif (O'zbek)"))

    # Rus tili
    name_ru = models.CharField(_("Название (Русский)"), max_length=200)
    short_description_ru = models.CharField(_("Краткое описание (Русский)"), max_length=300)
    description_ru = models.TextField(_("Полное описание (Русский)"))

    # Ingliz tili
    name_en = models.CharField(_("Name (English)"), max_length=200)
    short_description_en = models.CharField(_("Short description (English)"), max_length=300)
    description_en = models.TextField(_("Full description (English)"))

    # Qo'shimcha
    slug = models.SlugField(max_length=200, unique=True, db_index=True)  # ✅ FIXED
    price = models.DecimalField(
        _("Narxi"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]  # ✅ FIXED: validator
    )
    duration = models.PositiveIntegerField(
        _("Davomiyligi (daqiqa)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(5), MaxValueValidator(480)]  # ✅ FIXED: 5 daqiqadan 8 soatgacha
    )
    icon = models.CharField(_("Icon class"), max_length=100, default='bi bi-heart-pulse')
    image = models.ImageField(
        _("Rasm"),
        upload_to='services/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],  # ✅ FIXED
    )
    view_count = models.PositiveIntegerField(_("Ko'rilgan"), default=0)
    order = models.IntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)
    is_featured = models.BooleanField(_("Asosiyda ko'rsatish"), default=False, db_index=True)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("Xizmat")
        verbose_name_plural = _("Xizmatlar")
        ordering = ['order', '-created_at']
        indexes = [  # ✅ FIXED
            models.Index(fields=['slug']),
            models.Index(fields=['department', 'is_active']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        """✅ FIXED"""
        from django.utils.translation import get_language
        lang = get_language()
        return getattr(self, f'name_{lang}', self.name_uz)

    def save(self, *args, **kwargs):
        """✅ FIXED"""
        if not self.slug:
            base_slug = slugify(self.name_en) or slugify(self.name_uz, allow_unicode=True)
            self.slug = base_slug

            counter = 1
            while Service.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service-detail', kwargs={'pk': self.pk})

    def increment_view_count(self):
        """✅ FIXED: F() expression bilan atomic update"""
        from django.db.models import F
        Service.objects.filter(pk=self.pk).update(view_count=F('view_count') + 1)


class Doctor(models.Model):
    """Shifokorlar modeli"""
    first_name = models.CharField(_("Ism"), max_length=100)
    last_name = models.CharField(_("Familiya"), max_length=100)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)  # ✅ FIXED

    # O'zbek tili
    specialty_uz = models.CharField(_("Mutaxassisligi (O'zbek)"), max_length=200)
    bio_uz = models.TextField(_("Biografiya (O'zbek)"))
    education_uz = models.TextField(_("Ta'lim (O'zbek)"), blank=True)

    # Rus tili
    specialty_ru = models.CharField(_("Специальность (Русский)"), max_length=200)
    bio_ru = models.TextField(_("Биография (Русский)"))
    education_ru = models.TextField(_("Образование (Русский)"), blank=True)

    # Ingliz tili
    specialty_en = models.CharField(_("Specialty (English)"), max_length=200)
    bio_en = models.TextField(_("Biography (English)"))
    education_en = models.TextField(_("Education (English)"), blank=True)

    # Qo'shimcha
    photo = models.ImageField(
        _("Fotosurat"),
        upload_to='doctors/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],  # ✅ FIXED
    )
    phone = models.CharField(_("Telefon"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    experience_years = models.PositiveIntegerField(
        _("Tajriba (yil)"),
        default=0,
        validators=[MaxValueValidator(50)]  # ✅ FIXED: 50 yilgacha
    )

    # Many-to-Many bog'lanish
    departments = models.ManyToManyField(
        Department,
        related_name='doctors',
        verbose_name=_("Bo'limlar")
    )

    # Ijtimoiy tarmoqlar
    facebook = models.URLField(_("Facebook"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)

    order = models.IntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)
    is_featured = models.BooleanField(_("Asosiyda ko'rsatish"), default=False, db_index=True)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("Shifokor")
        verbose_name_plural = _("Shifokorlar")
        ordering = ['order', 'last_name', 'first_name']
        indexes = [  # ✅ FIXED
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """✅ FIXED"""
        if not self.slug:
            base_slug = slugify(f"{self.first_name}-{self.last_name}")
            self.slug = base_slug

            counter = 1
            while Doctor.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Mijozlar fikrlari"""
    name = models.CharField(_("Ism"), max_length=100)
    photo = models.ImageField(
        _("Fotosurat"),
        upload_to='testimonials/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],  # ✅ FIXED
    )

    # O'zbek tili
    position_uz = models.CharField(_("Lavozim/Kasb (O'zbek)"), max_length=200)
    text_uz = models.TextField(_("Fikr (O'zbek)"))

    # Rus tili
    position_ru = models.CharField(_("Должность (Русский)"), max_length=200)
    text_ru = models.TextField(_("Отзыв (Русский)"))

    # Ingliz tili
    position_en = models.CharField(_("Position (English)"), max_length=200)
    text_en = models.TextField(_("Testimonial (English)"))

    rating = models.IntegerField(
        _("Reyting"),
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)
    is_featured = models.BooleanField(_("Asosiyda ko'rsatish"), default=False)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)

    class Meta:
        verbose_name = _("Fikr")
        verbose_name_plural = _("Fikrlar")
        ordering = ['-created_at']
        indexes = [  # ✅ FIXED
            models.Index(fields=['is_active', 'is_featured']),
        ]

    def __str__(self):
        return f"{self.name} - {self.rating}★"


class Gallery(models.Model):
    """Galereya"""
    CATEGORY_CHOICES = [
        ('clinic', _('Klinika')),
        ('equipment', _('Jihozlar')),
        ('team', _('Jamoa')),
        ('patients', _('Bemorlar')),
        ('other', _('Boshqa')),
    ]

    # O'zbek tili
    title_uz = models.CharField(_("Sarlavha (O'zbek)"), max_length=200)

    # Rus tili
    title_ru = models.CharField(_("Заголовок (Русский)"), max_length=200)

    # Ingliz tili
    title_en = models.CharField(_("Title (English)"), max_length=200)

    image = models.ImageField(
        _("Rasm"),
        upload_to='gallery/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],  # ✅ FIXED
    )
    category = models.CharField(_("Kategoriya"), max_length=20, choices=CATEGORY_CHOICES, default='other',
                                db_index=True)
    order = models.IntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)

    class Meta:
        verbose_name = _("Galereya rasmi")
        verbose_name_plural = _("Galereya rasmlari")
        ordering = ['order', '-created_at']
        indexes = [  # ✅ FIXED
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        """✅ FIXED"""
        from django.utils.translation import get_language
        lang = get_language()
        return getattr(self, f'title_{lang}', self.title_uz)


class Appointment(models.Model):
    """Qabulga yozilish"""
    STATUS_CHOICES = [
        ('pending', _('Kutilmoqda')),
        ('confirmed', _('Tasdiqlangan')),
        ('completed', _('Yakunlangan')),
        ('cancelled', _('Bekor qilingan')),
    ]

    name = models.CharField(_("Ism"), max_length=100)
    phone = models.CharField(_("Telefon"), max_length=20)
    email = models.EmailField(_("Email"))

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments',
        verbose_name=_("Bo'lim")
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='appointments',
        verbose_name=_("Shifokor")
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='appointments',
        verbose_name=_("Xizmat")
    )

    date = models.DateField(_("Sana"))
    time = models.TimeField(_("Vaqt"))
    message = models.TextField(_("Xabar"), blank=True)

    status = models.CharField(_("Holat"), max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    admin_notes = models.TextField(_("Admin izohi"), blank=True)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("Qabul")
        verbose_name_plural = _("Qabullar")
        ordering = ['-date', '-time']
        indexes = [  # ✅ FIXED
            models.Index(fields=['status', 'date']),
            models.Index(fields=['doctor', 'date', 'time']),
        ]
        unique_together = [['doctor', 'date', 'time']]  # ✅ FIXED: Bir vaqtda bir shifokor

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"


class FAQ(models.Model):
    """Tez-tez so'raladigan savollar"""
    # O'zbek tili
    question_uz = models.CharField(_("Savol (O'zbek)"), max_length=500)
    answer_uz = models.TextField(_("Javob (O'zbek)"))

    # Rus tili
    question_ru = models.CharField(_("Вопрос (Русский)"), max_length=500)
    answer_ru = models.TextField(_("Ответ (Русский)"))

    # Ingliz tili
    question_en = models.CharField(_("Question (English)"), max_length=500)
    answer_en = models.TextField(_("Answer (English)"))

    order = models.IntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")
        ordering = ['order', '-created_at']

    def __str__(self):
        """✅ FIXED"""
        from django.utils.translation import get_language
        lang = get_language()
        return getattr(self, f'question_{lang}', self.question_uz)[:100]


class ContactMessage(models.Model):
    """Kontakt xabarlari"""
    name = models.CharField(_("Ism"), max_length=100)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Mavzu"), max_length=200)
    message = models.TextField(_("Xabar"))

    is_read = models.BooleanField(_("O'qilgan"), default=False, db_index=True)
    is_replied = models.BooleanField(_("Javob berilgan"), default=False)

    created_at = models.DateTimeField(_("Yaratilgan"), auto_now_add=True)

    class Meta:
        verbose_name = _("Xabar")
        verbose_name_plural = _("Xabarlar")
        ordering = ['-created_at']
        indexes = [  # ✅ FIXED
            models.Index(fields=['is_read', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class SiteSettings(models.Model):
    """Sayt sozlamalari"""
    # Sayt nomi
    site_name_uz = models.CharField(_("Sayt nomi (O'zbek)"), max_length=200, default="MediNest")
    site_name_ru = models.CharField(_("Название сайта (Русский)"), max_length=200, default="MediNest")
    site_name_en = models.CharField(_("Site name (English)"), max_length=200, default="MediNest")

    # Slogan
    tagline_uz = models.CharField(_("Slogan (O'zbek)"), max_length=300, blank=True)
    tagline_ru = models.CharField(_("Слоган (Русский)"), max_length=300, blank=True)
    tagline_en = models.CharField(_("Tagline (English)"), max_length=300, blank=True)

    # Biz haqimizda
    about_uz = models.TextField(_("Biz haqimizda (O'zbek)"), blank=True)
    about_ru = models.TextField(_("О нас (Русский)"), blank=True)
    about_en = models.TextField(_("About us (English)"), blank=True)

    # Kontakt
    phone_1 = models.CharField(_("Telefon 1"), max_length=20)
    phone_2 = models.CharField(_("Telefon 2"), max_length=20, blank=True)
    email = models.EmailField(_("Email"))

    address_uz = models.CharField(_("Manzil (O'zbek)"), max_length=500)
    address_ru = models.CharField(_("Адрес (Русский)"), max_length=500)
    address_en = models.CharField(_("Address (English)"), max_length=500)

    working_hours_uz = models.CharField(_("Ish vaqti (O'zbek)"), max_length=200, default="Dush-Juma: 09:00-20:00")
    working_hours_ru = models.CharField(_("Часы работы (Русский)"), max_length=200, default="Пн-Пт: 09:00-20:00")
    working_hours_en = models.CharField(_("Working hours (English)"), max_length=200, default="Mon-Fri: 09:00-20:00")

    # Ijtimoiy tarmoqlar
    facebook = models.URLField(_("Facebook"), blank=True)
    instagram = models.URLField(_("Instagram"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    youtube = models.URLField(_("YouTube"), blank=True)

    # Xarita
    google_maps_embed = models.TextField(_("Google Maps embed kodi"), blank=True)

    # Logo va favicon
    logo = models.ImageField(
        _("Logo"),
        upload_to='site/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'svg', 'webp'])],  # ✅ FIXED
    )
    favicon = models.ImageField(
        _("Favicon"),
        upload_to='site/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['ico', 'png'])],  # ✅ FIXED
    )

    # SEO
    meta_description_uz = models.TextField(_("Meta Description (O'zbek)"), max_length=160, blank=True)
    meta_description_ru = models.TextField(_("Meta Description (Русский)"), max_length=160, blank=True)
    meta_description_en = models.TextField(_("Meta Description (English)"), max_length=160, blank=True)

    meta_keywords_uz = models.CharField(_("Meta Keywords (O'zbek)"), max_length=500, blank=True)
    meta_keywords_ru = models.CharField(_("Meta Keywords (Русский)"), max_length=500, blank=True)
    meta_keywords_en = models.CharField(_("Meta Keywords (English)"), max_length=500, blank=True)

    updated_at = models.DateTimeField(_("O'zgartirilgan"), auto_now=True)

    class Meta:
        verbose_name = _("Sayt sozlamalari")
        verbose_name_plural = _("Sayt sozlamalari")

    def __str__(self):
        return "Sayt sozlamalari"

    def save(self, *args, **kwargs):
        """✅ FIXED: Faqat bitta instance bo'lishini ta'minlash"""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """✅ FIXED: Singleton pattern"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Statistic(models.Model):
    """Statistika"""
    # O'zbek tili
    label_uz = models.CharField(_("Nomi (O'zbek)"), max_length=200)

    # Rus tili
    label_ru = models.CharField(_("Название (Русский)"), max_length=200)

    # Ingliz tili
    label_en = models.CharField(_("Label (English)"), max_length=200)

    value = models.PositiveIntegerField(_("Qiymat"), default=0)
    icon = models.CharField(_("Icon class"), max_length=100, default='bi bi-heart')
    order = models.IntegerField(_("Tartib"), default=0)
    is_active = models.BooleanField(_("Faol"), default=True, db_index=True)

    class Meta:
        verbose_name = _("Statistika")
        verbose_name_plural = _("Statistikalar")
        ordering = ['order']

    def __str__(self):
        """✅ FIXED"""
        from django.utils.translation import get_language
        lang = get_language()
        return f"{getattr(self, f'label_{lang}', self.label_uz)}: {self.value}"