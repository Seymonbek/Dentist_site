from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    Department, Service, Doctor, Testimonial, Gallery,
    Appointment, FAQ, ContactMessage, SiteSettings, Statistic
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'slug', 'services_count', 'doctors_count', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name_uz', 'name_ru', 'name_en', 'description_uz', 'slug']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('O\'zbek tili', {
            'fields': ('name_uz', 'description_uz')
        }),
        ('Русский язык', {
            'fields': ('name_ru', 'description_ru')
        }),
        ('English', {
            'fields': ('name_en', 'description_en')
        }),
        ('Qo\'shimcha', {
            'fields': ('slug', 'icon', 'image', 'order', 'is_active')
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def services_count(self, obj):
        return obj.services.filter(is_active=True).count()

    services_count.short_description = 'Xizmatlar soni'

    def doctors_count(self, obj):
        return obj.doctors.filter(is_active=True).count()

    doctors_count.short_description = 'Shifokorlar soni'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _services_count=Count('services', distinct=True),
            _doctors_count=Count('doctors', distinct=True)
        )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'department', 'price_display', 'duration', 'view_count', 'is_featured', 'order',
                    'is_active']
    list_filter = ['department', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name_uz', 'name_ru', 'name_en', 'description_uz', 'slug']
    list_editable = ['order', 'is_active', 'is_featured']
    prepopulated_fields = {'slug': ('name_en',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']

    fieldsets = (
        ('O\'zbek tili', {
            'fields': ('name_uz', 'short_description_uz', 'description_uz')
        }),
        ('Русский язык', {
            'fields': ('name_ru', 'short_description_ru', 'description_ru')
        }),
        ('English', {
            'fields': ('name_en', 'short_description_en', 'description_en')
        }),
        ('Qo\'shimcha', {
            'fields': ('department', 'slug', 'price', 'duration', 'icon', 'image', 'order', 'is_active', 'is_featured',
                       'view_count')
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        if obj.price:
            try:
                cleaned_price = str(obj.price).replace("so'm", "").replace(",", "").strip()
                return format_html(
                    '<span style="color: green; font-weight: bold;">{:,.0f} so\'m</span>',
                    float(cleaned_price)
                )
            except ValueError:
                return obj.price  # yoki xatolikni ko‘rsatish
        return '-'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialty_uz', 'experience_years', 'phone', 'departments_list', 'is_featured',
                    'order', 'is_active']
    list_filter = ['is_active', 'is_featured', 'experience_years', 'departments', 'created_at']
    search_fields = ['first_name', 'last_name', 'specialty_uz', 'bio_uz', 'slug']
    list_editable = ['order', 'is_active', 'is_featured']
    filter_horizontal = ['departments']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'slug', 'photo', 'experience_years')
        }),
        ('O\'zbek tili', {
            'fields': ('specialty_uz', 'bio_uz', 'education_uz')
        }),
        ('Русский язык', {
            'fields': ('specialty_ru', 'bio_ru', 'education_ru')
        }),
        ('English', {
            'fields': ('specialty_en', 'bio_en', 'education_en')
        }),
        ('Kontaktlar', {
            'fields': ('phone', 'email')
        }),
        ('Ijtimoiy tarmoqlar', {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin'),
            'classes': ('collapse',)
        }),
        ('Qo\'shimcha', {
            'fields': ('departments', 'order', 'is_active', 'is_featured')
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def departments_list(self, obj):
        return ", ".join([dept.name_uz for dept in obj.departments.all()[:3]])

    departments_list.short_description = 'Bo\'limlar'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating_stars', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'text_uz', 'text_ru', 'text_en']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'photo', 'rating')
        }),
        ('O\'zbek tili', {
            'fields': ('position_uz', 'text_uz')
        }),
        ('Русский язык', {
            'fields': ('position_ru', 'text_ru')
        }),
        ('English', {
            'fields': ('position_en', 'text_en')
        }),
        ('Qo\'shimcha', {
            'fields': ('is_active', 'is_featured', 'created_at')
        }),
    )

    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="font-size: 16px;">{}</span>', stars)

    rating_stars.short_description = 'Reyting'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'category', 'image_preview', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title_uz', 'title_ru', 'title_en']
    list_editable = ['order', 'is_active']
    readonly_fields = ['image_preview', 'created_at']

    fieldsets = (
        ('O\'zbek tili', {
            'fields': ('title_uz',)
        }),
        ('Русский язык', {
            'fields': ('title_ru',)
        }),
        ('English', {
            'fields': ('title_en',)
        }),
        ('Qo\'shimcha', {
            'fields': ('category', 'image', 'image_preview', 'order', 'is_active', 'created_at')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
        return '-'

    image_preview.short_description = 'Rasm ko\'rinishi'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'department', 'doctor', 'date', 'time', 'status_badge', 'created_at', 'status']
    list_filter = ['status', 'department', 'doctor', 'date', 'created_at']
    search_fields = ['name', 'phone', 'email', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Qabul ma\'lumotlari', {
            'fields': ('department', 'doctor', 'service', 'date', 'time', 'message')
        }),
        ('Holat', {
            'fields': ('status', 'admin_notes')
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'completed': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )

    status_badge.short_description = 'Holat'

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
        self.message_user(request, f"{queryset.count()} ta qabul tasdiqlandi")

    mark_as_confirmed.short_description = "Tanlangan qabullarni tasdiqlash"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} ta qabul yakunlandi")

    mark_as_completed.short_description = "Tanlangan qabullarni yakunlash"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} ta qabul bekor qilindi")

    mark_as_cancelled.short_description = "Tanlangan qabullarni bekor qilish"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_uz_short', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question_uz', 'question_ru', 'question_en', 'answer_uz']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('O\'zbek tili', {
            'fields': ('question_uz', 'answer_uz')
        }),
        ('Русский язык', {
            'fields': ('question_ru', 'answer_ru')
        }),
        ('English', {
            'fields': ('question_en', 'answer_en')
        }),
        ('Qo\'shimcha', {
            'fields': ('order', 'is_active')
        }),
        ('Vaqt belgilari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def question_uz_short(self, obj):
        return obj.question_uz[:100] + '...' if len(obj.question_uz) > 100 else obj.question_uz

    question_uz_short.short_description = 'Savol'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read_badge', 'is_replied', 'created_at', 'is_read']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_replied']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Xabar ma\'lumotlari', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Holat', {
            'fields': ('is_read', 'is_replied', 'created_at')
        }),
    )

    actions = ['mark_as_read', 'mark_as_replied']

    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green;">✓ O\'qilgan</span>')
        return format_html('<span style="color: orange;">○ O\'qilmagan</span>')

    is_read_badge.short_description = 'Holat'

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} ta xabar o'qilgan deb belgilandi")

    mark_as_read.short_description = "O'qilgan deb belgilash"

    def mark_as_replied(self, request, queryset):
        queryset.update(is_replied=True)
        self.message_user(request, f"{queryset.count()} ta xabarga javob berilgan deb belgilandi")

    mark_as_replied.short_description = "Javob berilgan deb belgilash"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ['updated_at']

    fieldsets = (
        ('Sayt nomi va slogan', {
            'fields': (
                ('site_name_uz', 'site_name_ru', 'site_name_en'),
                ('tagline_uz', 'tagline_ru', 'tagline_en'),
            )
        }),
        ('Biz haqimizda', {
            'fields': ('about_uz', 'about_ru', 'about_en')
        }),
        ('Kontakt ma\'lumotlari', {
            'fields': (
                ('phone_1', 'phone_2', 'email'),
                ('address_uz', 'address_ru', 'address_en'),
                ('working_hours_uz', 'working_hours_ru', 'working_hours_en'),
            )
        }),
        ('Ijtimoiy tarmoqlar', {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin', 'youtube')
        }),
        ('Xarita', {
            'fields': ('google_maps_embed',)
        }),
        ('Logotiplar', {
            'fields': ('logo', 'favicon')
        }),
        ('SEO sozlamalari', {
            'fields': (
                ('meta_description_uz', 'meta_description_ru', 'meta_description_en'),
                ('meta_keywords_uz', 'meta_keywords_ru', 'meta_keywords_en'),
            ),
            'classes': ('collapse',)
        }),
        ('Vaqt belgilari', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['label_uz', 'value_display', 'icon', 'order', 'is_active', 'value']
    list_filter = ['is_active']
    search_fields = ['label_uz', 'label_ru', 'label_en']
    list_editable = ['order', 'is_active', 'value']

    fieldsets = (
        ('O\'zbek tili', {
            'fields': ('label_uz',)
        }),
        ('Русский язык', {
            'fields': ('label_ru',)
        }),
        ('English', {
            'fields': ('label_en',)
        }),
        ('Qo\'shimcha', {
            'fields': ('value', 'icon', 'order', 'is_active')
        }),
    )

    def value_display(self, obj):
        return format_html('<span style="font-weight: bold; color: blue; font-size: 16px;">{:,}</span>', obj.value)

    value_display.short_description = 'Qiymat'


# Admin site customization
admin.site.site_header = "DentaCare Admin Panel"
admin.site.site_title = "DentaCare Admin"
admin.site.index_title = "Boshqaruv paneli"