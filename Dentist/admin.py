"""
DentCare Stomatologiya Klinikasi - Admin Panel
===============================================
Professional Django admin konfiguratsiyasi
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum

from .models import (
    Department, Doctor, Service, Appointment,
    Testimonial, GalleryImage, ContactMessage, FAQ,
    WorkingHours, SiteSettings, About, DoctorLeave
)

# ============================================================================
# ADMIN CUSTOMIZATION
# ============================================================================

admin.site.site_header = "DentCare Admin Panel"
admin.site.site_title = "DentCare"
admin.site.index_title = "Boshqaruv Paneli"



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Bo'limlar admin paneli"""

    list_display = ['name', 'slug', 'doctor_count', 'service_count', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'full_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Asosiy', {
            'fields': ('name', 'slug', 'icon', 'description', 'full_description')
        }),
        ('Rasm', {
            'fields': ('image',)
        }),
        ('Holat', {
            'fields': ('is_active', 'order')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def doctor_count(self, obj):
        """Shifokorlar soni"""
        count = obj.doctors.count()
        return format_html(
            '<span style="color: green; font-weight: bold;">{}</span>',
            count
        )

    doctor_count.short_description = "Shifokorlar"

    def service_count(self, obj):
        """Xizmatlar soni"""
        count = obj.services.count()
        return format_html(
            '<span style="color: blue; font-weight: bold;">{}</span>',
            count
        )

    service_count.short_description = "Xizmatlar"


# ============================================================================
# DOCTOR ADMIN
# ============================================================================

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Shifokorlar admin paneli"""

    list_display = [
        'get_full_name', 'specialization', 'department',
        'patients_count', 'experience_years', 'rating',
        'is_featured', 'is_available', 'order'
    ]
    list_filter = [
        'department', 'gender', 'is_featured',
        'is_available', 'specialization', 'created_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'middle_name',
        'specialization', 'phone', 'bio'
    ]
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_editable = ['is_featured', 'is_available', 'order']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Shaxsiy', {
            'fields': (
                'user', 'first_name', 'last_name', 'middle_name',
                'slug', 'gender', 'photo', 'phone'
            )
        }),
        ('Ish Grafigi', {
            'fields': (
                ('work_start', 'work_end'),
                'consultation_duration',
            ),
            'description': 'Ish vaqti va konsultatsiya davomiyligi'
        }),
        ('Ish Kunlari', {
            'fields': (
                ('is_mon', 'is_tue', 'is_wed'),
                ('is_thu', 'is_fri', 'is_sat', 'is_sun'),
            ),
        }),
        ('Professional', {
            'fields': (
                'department', 'specialization', 'degree',
                'experience_years', 'bio', 'education', 'achievements'
            )
        }),
        ('Statistika', {
            'fields': (
                'rating', 'patients_count',
                'is_available', 'is_featured', 'order'
            )
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        """To'liq ism"""
        return f"Dr. {obj.first_name} {obj.last_name}"

    get_full_name.short_description = "Ism"
    get_full_name.admin_order_field = 'last_name'

    actions = ['make_featured', 'make_available', 'make_unavailable']

    def make_featured(self, request, queryset):
        """Featured qilish"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} ta shifokor featured qilindi')

    make_featured.short_description = "Featured qilish"

    def make_available(self, request, queryset):
        """Mavjud qilish"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} ta shifokor mavjud qilindi')

    make_available.short_description = "Mavjud qilish"

    def make_unavailable(self, request, queryset):
        """Mavjud emasligini belgilash"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} ta shifokor mavjud emas qilindi')

    make_unavailable.short_description = "Mavjud emas qilish"

    def get_queryset(self, request):
        """Shifokor faqat o'zini ko'radi"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        """Shifokor o'ziga reyting bera olmaydi"""
        if request.user.is_superuser:
            return self.readonly_fields
        return [
            'user', 'rating', 'patients_count', 'is_featured',
            'order', 'is_available', 'slug', 'created_at', 'updated_at'
        ]


# ============================================================================
# DOCTOR LEAVE ADMIN
# ============================================================================

@admin.register(DoctorLeave)
class DoctorLeaveAdmin(admin.ModelAdmin):
    """Shifokorlar dam olish kunlari"""

    list_display = ['doctor', 'date', 'reason']
    list_filter = ['doctor', 'date']
    search_fields = ['doctor__first_name', 'doctor__last_name', 'reason']
    date_hierarchy = 'date'

    def get_queryset(self, request):
        """Shifokor faqat o'zini ko'radi"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor__user=request.user)

    def save_model(self, request, obj, form, change):
        """Avtomatik doctor belgilash"""
        if not request.user.is_superuser:
            obj.doctor = request.user.doctor_profile
        super().save_model(request, obj, form, change)


# ============================================================================
# SERVICE ADMIN
# ============================================================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Xizmatlar admin paneli"""

    list_display = [
        'name', 'department', 'price_from', 'price_to',
        'duration', 'is_popular', 'is_active', 'order'
    ]
    list_filter = ['department', 'is_popular', 'is_active', 'created_at']
    search_fields = ['name', 'short_description', 'full_description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_popular', 'is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Asosiy', {
            'fields': (
                'name', 'slug', 'department',
                'icon', 'short_description', 'full_description'
            )
        }),
        ('Narx va Vaqt', {
            'fields': ('price_from', 'price_to', 'duration')
        }),
        ('Rasm', {
            'fields': ('image',)
        }),
        ('Holat', {
            'fields': ('is_popular', 'is_active', 'order')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_popular', 'make_not_popular']

    def make_popular(self, request, queryset):
        """Mashhur qilish"""
        updated = queryset.update(is_popular=True)
        self.message_user(request, f'{updated} ta xizmat mashhur qilindi')

    make_popular.short_description = "Mashhur qilish"

    def make_not_popular(self, request, queryset):
        """Mashhur emasligini belgilash"""
        updated = queryset.update(is_popular=False)
        self.message_user(request, f'{updated} ta xizmat mashhur emas qilindi')

    make_not_popular.short_description = "Mashhur emas qilish"


# ============================================================================
# APPOINTMENT ADMIN
# ============================================================================

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Qabulga yozilish admin paneli"""

    list_display = [
        'name', 'phone', 'department', 'doctor',
        'appointment_date', 'appointment_time', 'status', 'created_at'
    ]
    list_filter = ['status', 'department', 'doctor', 'appointment_date', 'created_at']
    search_fields = ['name', 'phone', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'appointment_date'

    fieldsets = (
        ('Bemor', {
            'fields': ('name', 'phone')
        }),
        ('Qabul', {
            'fields': (
                'department', 'doctor', 'service',
                'appointment_date', 'appointment_time'
            )
        }),
        ('Xabar', {
            'fields': ('message',)
        }),
        ('Holat', {
            'fields': ('status', 'notes')
        }),
        ('Vaqt', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['confirm_appointments', 'cancel_appointments', 'complete_appointments']

    def confirm_appointments(self, request, queryset):
        """Tasdiqlash"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} ta qabul tasdiqlandi')

    confirm_appointments.short_description = "Tasdiqlash"

    def cancel_appointments(self, request, queryset):
        """Bekor qilish"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} ta qabul bekor qilindi')

    cancel_appointments.short_description = "Bekor qilish"

    def complete_appointments(self, request, queryset):
        """Yakunlash"""
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} ta qabul yakunlandi')

    complete_appointments.short_description = "Yakunlash"

    def get_queryset(self, request):
        """Shifokor faqat o'z qabullarini ko'radi"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(doctor__user=request.user)


# ============================================================================
# TESTIMONIAL ADMIN
# ============================================================================

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Fikrlar admin paneli"""

    list_display = [
        'name', 'position', 'get_stars',
        'is_featured', 'is_active', 'created_at'
    ]
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'position', 'comment']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Bemor', {
            'fields': ('name', 'position', 'photo')
        }),
        ('Fikr', {
            'fields': ('rating', 'comment')
        }),
        ('Holat', {
            'fields': ('is_featured', 'is_active')
        }),
    )

    def get_stars(self, obj):
        """Yulduzlar ko'rinishi"""
        stars = '⭐' * obj.rating
        return format_html(
            '<span style="color: gold; font-size: 16px;">{}</span>',
            stars
        )

    get_stars.short_description = 'Reyting'


# ============================================================================
# GALLERY ADMIN
# ============================================================================

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Galereya admin paneli"""

    list_display = [
        'title', 'category', 'image_preview',
        'is_active', 'order', 'created_at'
    ]
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'image_preview']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Asosiy', {
            'fields': ('title', 'description', 'category')
        }),
        ('Rasm', {
            'fields': ('image', 'image_preview')
        }),
        ('Holat', {
            'fields': ('is_active', 'order')
        }),
    )

    def image_preview(self, obj):
        """Rasm ko'rinishi"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px;" />',
                obj.image.url
            )
        return "Rasm yo'q"

    image_preview.short_description = 'Ko\'rinish'


# ============================================================================
# CONTACT MESSAGE ADMIN
# ============================================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Xabarlar admin paneli"""

    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Yuboruvchi', {
            'fields': ('name', 'email')
        }),
        ('Xabar', {
            'fields': ('subject', 'message')
        }),
        ('Holat', {
            'fields': ('is_read',)
        }),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        """O'qilgan deb belgilash"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} ta xabar o\'qilgan')

    mark_as_read.short_description = "O'qilgan"

    def mark_as_unread(self, request, queryset):
        """O'qilmagan deb belgilash"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} ta xabar o\'qilmagan')

    mark_as_unread.short_description = "O'qilmagan"


# ============================================================================
# FAQ ADMIN
# ============================================================================

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """FAQ admin paneli"""

    list_display = ['question', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Savol-Javob', {
            'fields': ('question', 'answer', 'category')
        }),
        ('Holat', {
            'fields': ('is_active', 'order')
        }),
    )


# ============================================================================
# WORKING HOURS ADMIN
# ============================================================================

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    """Ish vaqti admin paneli"""

    list_display = ['get_day_display', 'is_working_day', 'opening_time', 'closing_time']
    list_editable = ['is_working_day', 'opening_time', 'closing_time']
    ordering = ['day']

    def has_add_permission(self, request):
        """Faqat 7 kun"""
        return WorkingHours.objects.count() < 7

    def has_delete_permission(self, request, obj=None):
        """O'chirish mumkin emas"""
        return False


# ============================================================================
# SITE SETTINGS ADMIN
# ============================================================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Sozlamalar admin paneli"""

    fieldsets = (
        ('Asosiy', {
            'fields': ('site_name', 'tagline', 'phone', 'email', 'address')
        }),
        ('Ijtimoiy', {
            'fields': ('facebook', 'instagram', 'telegram', 'youtube')
        }),
        ('Dizayn', {
            'fields': ('logo', 'favicon', 'chief_doctor_image', 'map_embed', 'footer_text')
        }),
    )

    def has_add_permission(self, request):
        """Faqat 1 ta sozlama"""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """O'chirish mumkin emas"""
        return False


# ============================================================================
# ABOUT ADMIN
# ============================================================================

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """Biz haqimizda admin paneli"""

    list_display = ['title']

    def has_add_permission(self, request):
        """Faqat 1 ta"""
        return not About.objects.exists()