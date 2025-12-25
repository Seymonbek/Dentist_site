"""
Barcha formalar va validatsiyalar
"""

from django import forms
from django.core.exceptions import ValidationError
from datetime import date
import re

from .models import Appointment, ContactMessage, Department, Doctor, Service


class AppointmentForm(forms.ModelForm):
    """Qabulga yozilish formasi"""

    class Meta:
        model = Appointment
        fields = [
            'name', 'phone', 'department', 'doctor',
            'service', 'appointment_date', 'appointment_time', 'message'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "To'liq ismingiz",
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567',
                'required': True
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'service': forms.Select(attrs={
                'class': 'form-select'
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': date.today().isoformat(),
                'required': True
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': "Shikoyatingiz yoki qo'shimcha ma'lumot (ixtiyoriy)"
            })
        }

        labels = {
            'name': "To'liq Ism",
            'phone': 'Telefon',
            'department': "Bo'lim",
            'doctor': 'Shifokor (ixtiyoriy)',
            'service': 'Xizmat (ixtiyoriy)',
            'appointment_date': 'Sana',
            'appointment_time': 'Vaqt (ixtiyoriy)',
            'message': 'Xabar (ixtiyoriy)'
        }

        help_texts = {
            'phone': '+998901234567 formatida kiriting',
            'appointment_date': 'Qabulga borishni istagan sanangizni tanlang',
        }

    def __init__(self, *args, **kwargs):
        """Form initialization"""
        super().__init__(*args, **kwargs)

        # Faqat faol bo'limlar
        self.fields['department'].queryset = Department.objects.filter(
            is_active=True
        ).order_by('order', 'name')

        # Faqat mavjud shifokorlar
        self.fields['doctor'].queryset = Doctor.objects.filter(
            is_available=True
        ).select_related('department').order_by('order', 'last_name')

        self.fields['doctor'].required = False
        self.fields['doctor'].empty_label = "Shifokor tanlang (ixtiyoriy)"

        # Faqat faol xizmatlar
        self.fields['service'].queryset = Service.objects.filter(
            is_active=True
        ).select_related('department').order_by('order', 'name')

        self.fields['service'].required = False
        self.fields['service'].empty_label = "Xizmat tanlang (ixtiyoriy)"

        # Ixtiyoriy maydonlar
        self.fields['message'].required = False
        self.fields['appointment_time'].required = False

    # ========================================================================
    # FIELD VALIDATIONS
    # ========================================================================

    def clean_name(self):
        """Ism validatsiyasi"""
        name = self.cleaned_data.get('name')

        if not name:
            raise ValidationError("Ism majburiy maydon")

        # Bo'sh joylarni tozalash
        name = ' '.join(name.split())

        if len(name) < 3:
            raise ValidationError("Ism kamida 3 ta harfdan iborat bo'lishi kerak")

        if name.isdigit():
            raise ValidationError("Ism faqat raqamlardan iborat bo'lishi mumkin emas")

        # Faqat harflar va bo'shliqlar
        if not re.match(r'^[a-zA-Z\s\'\"\u0400-\u04FF]+$', name):
            raise ValidationError("Ism faqat harflardan iborat bo'lishi kerak")

        return name

    def clean_phone(self):
        """Telefon validatsiyasi"""
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise ValidationError("Telefon raqam majburiy")

        # Bo'shliqlar va belgilarni olib tashlash
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # +998XXXXXXXXX yoki 998XXXXXXXXX
        pattern = r'^\+?998\d{9}$'
        if not re.match(pattern, phone):
            raise ValidationError(
                "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak. "
                "Masalan: +998901234567"
            )

        # + qo'shish
        if not phone.startswith('+'):
            phone = '+' + phone

        return phone

    def clean_appointment_date(self):
        """Sana validatsiyasi"""
        appointment_date = self.cleaned_data.get('appointment_date')

        if not appointment_date:
            raise ValidationError("Qabul sanasini tanlang")

        if appointment_date < date.today():
            raise ValidationError(
                f"Qabul sanasi o'tgan bo'lishi mumkin emas! "
                f"Minimal sana: {date.today().strftime('%d.%m.%Y')}"
            )

        # Maksimal 3 oy oldinga
        max_date = date.today().replace(month=date.today().month + 3)
        if appointment_date > max_date:
            raise ValidationError(
                f"Qabul sanasi maksimal {max_date.strftime('%d.%m.%Y')} gacha bo'lishi mumkin"
            )

        return appointment_date

    def clean_appointment_time(self):
        """Vaqt validatsiyasi (ixtiyoriy)"""
        appointment_time = self.cleaned_data.get('appointment_time')
        return appointment_time

    # ========================================================================
    # MULTI-FIELD VALIDATION
    # ========================================================================

    def clean(self):
        """Ko'p maydonli validatsiya"""
        cleaned_data = super().clean()

        department = cleaned_data.get('department')
        doctor = cleaned_data.get('doctor')
        service = cleaned_data.get('service')

        # Shifokor va bo'lim mosligini tekshirish
        if doctor and department:
            if doctor.department != department:
                raise ValidationError({
                    'doctor': f"Bu shifokor {doctor.department.name} bo'limiga tegishli, "
                              f"{department.name} emas!"
                })

        # Xizmat va bo'lim mosligini tekshirish
        if service and department:
            if service.department != department:
                raise ValidationError({
                    'service': f"Bu xizmat {service.department.name} bo'limiga tegishli, "
                               f"{department.name} emas!"
                })

        return cleaned_data


# ============================================================================
# CONTACT FORM
# ============================================================================

class ContactForm(forms.ModelForm):
    """Bog'lanish formasi"""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingiz',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xabar mavzusi',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Xabaringizni yozing...',
                'required': True
            })
        }

        labels = {
            'name': 'Ism',
            'email': 'Email',
            'subject': 'Mavzu',
            'message': 'Xabar'
        }

        help_texts = {
            'email': 'Sizning email manzilingiz',
            'message': 'Kamida 20 ta belgi kiriting',
        }

    # ========================================================================
    # FIELD VALIDATIONS
    # ========================================================================

    def clean_name(self):
        """Ism validatsiyasi"""
        name = self.cleaned_data.get('name')

        if not name:
            raise ValidationError("Ism majburiy maydon")

        # Bo'sh joylarni tozalash
        name = ' '.join(name.split())

        if len(name) < 3:
            raise ValidationError("Ism kamida 3 ta harfdan iborat bo'lishi kerak")

        if len(name) > 100:
            raise ValidationError("Ism juda uzun (maksimal 100 ta belgi)")

        return name

    def clean_email(self):
        """Email validatsiyasi"""
        email = self.cleaned_data.get('email')

        if not email:
            raise ValidationError("Email majburiy maydon")

        # Kichik harf va bo'sh joylarni olib tashlash
        email = email.lower().strip()

        # Django avtomatik email formatini tekshiradi
        # Lekin qo'shimcha tekshiruv
        if '@' not in email or '.' not in email.split('@')[1]:
            raise ValidationError("Email manzil noto'g'ri formatda")

        return email

    def clean_subject(self):
        """Mavzu validatsiyasi"""
        subject = self.cleaned_data.get('subject')

        if not subject:
            raise ValidationError("Mavzu majburiy maydon")

        subject = ' '.join(subject.split())

        if len(subject) < 5:
            raise ValidationError("Mavzu kamida 5 ta harfdan iborat bo'lishi kerak")

        if len(subject) > 200:
            raise ValidationError("Mavzu juda uzun (maksimal 200 ta belgi)")

        return subject

    def clean_message(self):
        """Xabar validatsiyasi"""
        message = self.cleaned_data.get('message')

        if not message:
            raise ValidationError("Xabar majburiy maydon")

        message = message.strip()

        if len(message) < 20:
            raise ValidationError(
                f"Xabar juda qisqa. Kamida 20 ta belgi kiriting. "
                f"Hozir: {len(message)} ta belgi"
            )

        if len(message) > 5000:
            raise ValidationError(
                f"Xabar juda uzun (maksimal 5000 ta belgi). "
                f"Hozir: {len(message)} ta belgi"
            )

        return message


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_uzbek_phone(phone):
    """
    O'zbekiston telefon raqamini tekshirish
    Returns: Formatlangan telefon (+998XXXXXXXXX) yoki ValidationError
    """
    # Bo'sh joylar va maxsus belgilarni olib tashlash
    phone = re.sub(r'[^\d+]', '', phone)

    # Pattern: +998 + 9 ta raqam
    pattern = r'^\+?998\d{9}$'

    if not re.match(pattern, phone):
        raise ValidationError(
            "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
        )

    # + qo'shish agar yo'q bo'lsa
    if not phone.startswith('+'):
        phone = '+' + phone

    return phone