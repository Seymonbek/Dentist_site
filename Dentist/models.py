from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify



class Department(models.Model):
    """Klinika bo'limlari (Terapiya, Ortopediya, Ortodontiya va h.k.)"""

    name = models.CharField(max_length=200, verbose_name="Bo'lim nomi")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL slug")
    icon = models.CharField(max_length=50, verbose_name="Icon class", default="fas fa-tooth", help_text="FontAwesome icon class")
    description = models.TextField(verbose_name="Qisqa ta'rif")
    full_description = models.TextField(verbose_name="To'liq ta'rif", blank=True)
    image = models.ImageField(upload_to="departments/", verbose_name="Rasm", blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami",help_text="Ko'rsatish tartibi (kichik raqam birinchi)")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('department_detail', kwargs={'slug': self.slug})


class Doctor(models.Model):
    """Shifokorlar ma'lumotlari"""

    GENDER_CHOICES = [
        ('M', 'Erkak'),
        ('F', 'Ayol'),
    ]

    # User relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True, verbose_name="Foydalanuvchi")

    # Shaxsiy ma'lumotlar
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    middle_name = models.CharField(max_length=100, verbose_name="Otasining ismi", blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL slug")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Jinsi")
    photo = models.ImageField(upload_to="doctors/", verbose_name="Rasm")

    # Professional ma'lumotlar
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="doctors", verbose_name="Bo'lim")
    specialization = models.CharField(max_length=200, verbose_name="Mutaxassislik")
    degree = models.CharField(max_length=200, verbose_name="Ilmiy daraja", blank=True)
    experience_years = models.IntegerField(verbose_name="Tajriba yili", validators=[MinValueValidator(0)])
    bio = models.TextField(verbose_name="Biografiya")
    education = models.TextField(verbose_name="Ta'lim", blank=True)
    achievements = models.TextField(verbose_name="Yutuqlar", blank=True)

    # Ish grafigi
    work_start = models.TimeField(default="09:00", verbose_name="Ish boshlash vaqti")
    work_end = models.TimeField(default="18:00", verbose_name="Ish tugash vaqti")
    consultation_duration = models.PositiveIntegerField(default=30, verbose_name="Konsultatsiya davomiyligi (daqiqa)")

    # Ish kunlari
    is_mon = models.BooleanField(default=True, verbose_name="Dushanba")
    is_tue = models.BooleanField(default=True, verbose_name="Seshanba")
    is_wed = models.BooleanField(default=True, verbose_name="Chorshanba")
    is_thu = models.BooleanField(default=True, verbose_name="Payshanba")
    is_fri = models.BooleanField(default=True, verbose_name="Juma")
    is_sat = models.BooleanField(default=False, verbose_name="Shanba")
    is_sun = models.BooleanField(default=False, verbose_name="Yakshanba")

    # Aloqa
    phone = models.CharField(max_length=20, verbose_name="Telefon",
        validators=[RegexValidator(regex=r'^\+?998\d{9}$', message="Telefon +998XXXXXXXXX formatida bo'lishi kerak")]
    )

    # Statistika
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="Reyting", validators=[MinValueValidator(0), MaxValueValidator(5)])
    patients_count = models.PositiveIntegerField(default=0, verbose_name="Bemorlar soni")

    # Status
    is_available = models.BooleanField(default=True, verbose_name="Mavjud")
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy sahifada")
    order = models.IntegerField(default=0, verbose_name="Tartib raqami")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Shifokor"
        verbose_name_plural = "Shifokorlar"
        ordering = ['order', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_available', 'is_featured']),
            models.Index(fields=['department', 'is_available']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)

    def get_full_name(self):
        """To'liq ism"""
        return f"{self.first_name} {self.last_name}"

    def get_working_days(self):
        """Ish kunlari ro'yxati"""
        days = []
        day_map = {
            'is_mon': 'Dushanba',
            'is_tue': 'Seshanba',
            'is_wed': 'Chorshanba',
            'is_thu': 'Payshanba',
            'is_fri': 'Juma',
            'is_sat': 'Shanba',
            'is_sun': 'Yakshanba',
        }
        for field, name in day_map.items():
            if getattr(self, field):
                days.append(name)
        return ', '.join(days)


class DoctorLeave(models.Model):
    """Shifokorlarning dam olish kunlari"""

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='leaves',
        verbose_name="Shifokor"
    )
    date = models.DateField(
        verbose_name="Sana"
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Sabab"
    )

    class Meta:
        verbose_name = "Dam olish kuni"
        verbose_name_plural = "Dam olish kunlari"
        unique_together = ['doctor', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.date}"


class Service(models.Model):
    """Klinika xizmatlari"""

    name = models.CharField(
        max_length=200,
        verbose_name="Xizmat nomi"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="URL slug"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Bo'lim"
    )
    icon = models.CharField(
        max_length=50,
        verbose_name="Icon class",
        default="fas fa-tooth"
    )

    # Ta'rif
    short_description = models.TextField(
        verbose_name="Qisqa ta'rif"
    )
    full_description = models.TextField(
        verbose_name="To'liq ta'rif",
        blank=True
    )

    # Narx va vaqt
    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Narx (dan)",
        null=True,
        blank=True
    )
    price_to = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Narx (gacha)",
        null=True,
        blank=True
    )
    duration = models.IntegerField(
        verbose_name="Davomiyligi (daqiqa)",
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="services/",
        verbose_name="Rasm",
        blank=True,
        null=True
    )

    # Status
    is_popular = models.BooleanField(
        default=False,
        verbose_name="Mashhur"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Tartib"
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan"
    )

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_popular']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})

    def get_price_display(self):
        """Narx formati"""
        if self.price_from and self.price_to:
            return f"{self.price_from:,.0f} - {self.price_to:,.0f} so'm"
        elif self.price_from:
            return f"{self.price_from:,.0f} so'm dan"
        return "Narx individual"

    def get_duration_display(self):
        """Vaqt formati"""
        if self.duration:
            return f"{self.duration} daqiqa"
        return "Vaqt individual"


# ============================================================================
# QABULGA YOZILISH
# ============================================================================

class Appointment(models.Model):
    """Bemorlar qabulga yozilish"""

    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
        ('completed', 'Yakunlangan'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?998\d{9}$',
        message="Telefon +998XXXXXXXXX formatida bo'lishi kerak"
    )

    # Bemor ma'lumotlari
    name = models.CharField(
        max_length=200,
        verbose_name="To'liq ism"
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        verbose_name="Telefon"
    )

    # Qabul tafsilotlari
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Bo'lim"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Shifokor"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Xizmat"
    )
    appointment_date = models.DateField(
        verbose_name="Qabul sanasi"
    )
    appointment_time = models.TimeField(
        verbose_name="Qabul vaqti",
        null=True,
        blank=True
    )
    message = models.TextField(
        verbose_name="Xabar",
        blank=True
    )

    # Holat
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Holat"
    )
    notes = models.TextField(
        verbose_name="Admin eslatmalari",
        blank=True
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan"
    )

    class Meta:
        verbose_name = "Qabul"
        verbose_name_plural = "Qabullar"
        ordering = ['-appointment_date', '-created_at']
        indexes = [
            models.Index(fields=['status', 'appointment_date']),
            models.Index(fields=['doctor', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.name} - {self.appointment_date} ({self.get_status_display()})"

    def clean(self):
        """Validatsiya"""
        if self.appointment_date and self.appointment_time:
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(self.appointment_date, self.appointment_time)
            )
            if appointment_datetime < timezone.now():
                raise ValidationError("Qabul vaqti o'tgan bo'lishi mumkin emas!")

        if self.doctor and self.department:
            if self.doctor.department != self.department:
                raise ValidationError({
                    'doctor': f"Bu shifokor {self.doctor.department.name} bo'limiga tegishli!"
                })


# ============================================================================
# BOSHQA MODELLAR
# ============================================================================

class Testimonial(models.Model):
    """Bemorlar fikrlari"""

    name = models.CharField(
        max_length=200,
        verbose_name="Ism"
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Kasb",
        blank=True
    )
    photo = models.ImageField(
        upload_to="testimonials/",
        verbose_name="Rasm",
        blank=True,
        null=True
    )
    rating = models.IntegerField(
        verbose_name="Reyting",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(
        verbose_name="Fikr"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Asosiy sahifa"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan"
    )

    class Meta:
        verbose_name = "Fikr"
        verbose_name_plural = "Fikrlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.rating}★"

    def get_stars(self):
        """Yulduzlar"""
        return '★' * self.rating + '☆' * (5 - self.rating)


class GalleryImage(models.Model):
    """Galereya"""

    CATEGORY_CHOICES = [
        ('clinic', 'Klinika'),
        ('equipment', 'Uskunalar'),
        ('staff', 'Shifokorlar'),
        ('other', 'Boshqa'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name="Sarlavha"
    )
    description = models.TextField(
        verbose_name="Ta'rif",
        blank=True
    )
    image = models.ImageField(
        upload_to='gallery/',
        verbose_name="Rasm"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='clinic',
        verbose_name="Kategoriya"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Tartib"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan"
    )

    class Meta:
        verbose_name = "Galereya rasmi"
        verbose_name_plural = "Galereya"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Bog'lanish xabarlari"""

    name = models.CharField(
        max_length=200,
        verbose_name="Ism"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    subject = models.CharField(
        max_length=200,
        verbose_name="Mavzu"
    )
    message = models.TextField(
        verbose_name="Xabar"
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="O'qilgan"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan"
    )

    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class FAQ(models.Model):
    """Savol-javoblar"""

    CATEGORY_CHOICES = [
        ('general', 'Umumiy'),
        ('treatment', 'Davolash'),
        ('appointment', 'Qabul'),
        ('payment', "To'lov"),
        ('other', 'Boshqa'),
    ]

    question = models.CharField(
        max_length=500,
        verbose_name="Savol"
    )
    answer = models.TextField(
        verbose_name="Javob"
    )
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='general',
        verbose_name="Kategoriya"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Faol"
    )
    order = models.IntegerField(
        default=0,
        verbose_name="Tartib"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan"
    )

    class Meta:
        verbose_name = "Savol-Javob"
        verbose_name_plural = "Savol-Javoblar"
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class WorkingHours(models.Model):
    """Ish vaqti"""

    DAY_CHOICES = [
        (0, 'Dushanba'),
        (1, 'Seshanba'),
        (2, 'Chorshanba'),
        (3, 'Payshanba'),
        (4, 'Juma'),
        (5, 'Shanba'),
        (6, 'Yakshanba'),
    ]

    day = models.IntegerField(
        choices=DAY_CHOICES,
        unique=True,
        verbose_name="Kun"
    )
    is_working_day = models.BooleanField(
        default=True,
        verbose_name="Ish kuni"
    )
    opening_time = models.TimeField(
        verbose_name="Ochilish",
        null=True,
        blank=True
    )
    closing_time = models.TimeField(
        verbose_name="Yopilish",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Ish vaqti"
        verbose_name_plural = "Ish vaqtlari"
        ordering = ['day']

    def __str__(self):
        day_name = self.get_day_display()
        if self.is_working_day and self.opening_time and self.closing_time:
            return f"{day_name}: {self.opening_time.strftime('%H:%M')} - {self.closing_time.strftime('%H:%M')}"
        return f"{day_name}: Yopiq"


class SiteSettings(models.Model):
    """Sayt sozlamalari (singleton)"""

    site_name = models.CharField(
        max_length=200,
        verbose_name="Sayt nomi",
        default="DentCare"
    )
    tagline = models.CharField(
        max_length=500,
        verbose_name="Shior",
        blank=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Telefon"
    )
    email = models.EmailField(
        verbose_name="Email"
    )
    address = models.TextField(
        verbose_name="Manzil"
    )

    # Ijtimoiy tarmoqlar
    facebook = models.URLField(verbose_name="Facebook", blank=True)
    instagram = models.URLField(verbose_name="Instagram", blank=True)
    telegram = models.URLField(verbose_name="Telegram", blank=True)
    youtube = models.URLField(verbose_name="YouTube", blank=True)

    map_embed = models.TextField(
        verbose_name="Google Maps",
        blank=True
    )
    logo = models.ImageField(
        upload_to='site/',
        verbose_name="Logo",
        blank=True,
        null=True
    )
    favicon = models.ImageField(
        upload_to='site/',
        verbose_name="Favicon",
        blank=True,
        null=True
    )
    footer_text = models.TextField(
        verbose_name="Footer",
        blank=True
    )
    chief_doctor_image = models.ImageField(
        upload_to='settings/',
        verbose_name="Bosh shifokor rasmi",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Sozlama"
        verbose_name_plural = "Sozlamalar"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Faqat bitta SiteSettings bo\'lishi mumkin')
        super().save(*args, **kwargs)


class About(models.Model):
    """Biz haqimizda"""

    title = models.CharField(
        max_length=200,
        verbose_name="Sarlavha"
    )
    description = models.TextField(
        verbose_name="Ta'rif"
    )

    class Meta:
        verbose_name = "Biz haqimizda"
        verbose_name_plural = "Biz haqimizda"

    def __str__(self):
        return self.title