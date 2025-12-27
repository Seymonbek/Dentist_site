"""
Barcha formalar va validatsiyalar
"""

from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import re

from .models import Appointment, ContactMessage, Department, Doctor, Service


class AppointmentForm(forms.ModelForm):
    """Qabulga yozilish formasi"""

    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'department', 'doctor','service', 'appointment_date', 'appointment_time', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "To'liq ismingiz",
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567',
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-select',
            }),
            'service': forms.Select(attrs={
                'class': 'form-select',
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
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
            'doctor': 'Shifokor',
            'service': 'Xizmat',
            'appointment_date': 'Sana',
            'appointment_time': 'Vaqt',
            'message': 'Xabar (ixtiyoriy)'
        }

        help_texts = {
            'phone': '+998901234567 formatida kiriting',
            'appointment_date': 'Qabulga borishni istagan sanangizni tanlang',
        }

    def __init__(self, *args, **kwargs):
        """Form initialization"""
        super().__init__(*args, **kwargs)

        # Dinamik min sana
        self.fields['appointment_date'].widget.attrs['min'] = date.today().isoformat()

        # Faqat faol bo'limlar
        self.fields['department'].queryset = Department.objects.filter(is_active=True).order_by('order', 'name')
        self.fields['department'].required = True

        # Faqat mavjud shifokorlar
        self.fields['doctor'].queryset = Doctor.objects.filter(is_available=True).select_related('department').order_by('order', 'last_name')
        self.fields['doctor'].required = True
        self.fields['doctor'].empty_label = "Shifokor tanlang"

        # Faqat faol xizmatlar
        self.fields['service'].queryset = Service.objects.filter(is_active=True).select_related('department').order_by('order', 'name')
        self.fields['service'].required = True
        self.fields['service'].empty_label = "Xizmat tanlang"

        # Sana majburiy
        self.fields['appointment_date'].required = True

        # Vaqt majburiy
        self.fields['appointment_time'].required = True

        # Xabar ixtiyoriy
        self.fields['message'].required = False

    def clean_name(self):
        """Ism validatsiyasi"""
        name = self.cleaned_data.get('name')

        if not name:
            raise ValidationError("Ism majburiy maydon")

        name = ' '.join(name.split())

        if len(name) < 3:
            raise ValidationError("Ism kamida 3 ta harfdan iborat bo'lishi kerak")

        if name.isdigit():
            raise ValidationError("Ism faqat raqamlardan iborat bo'lishi mumkin emas")

        if not re.match(r'^[a-zA-Z\u0400-\u04FF\s\'"-]+$', name):
            raise ValidationError("Ism faqat harflardan iborat bo'lishi kerak")

        return name

    def clean_phone(self):
        """Telefon validatsiyasi"""
        phone = self.cleaned_data.get('phone')
        return validate_uzbek_phone(phone)


    def clean_appointment_date(self):
        """Sana validatsiyasi - 12-oy xatoligi tuzatilgan varianti"""
        appointment_date = self.cleaned_data.get('appointment_date')

        if not appointment_date:
            raise ValidationError("Qabul sanasini tanlang")

        today = date.today()

        # 1. O'tgan sanani tekshirish
        if appointment_date < today:
            raise ValidationError(
                f"Qabul sanasi o'tgan bo'lishi mumkin emas! "
                f"Minimal sana: {today.strftime('%d.%m.%Y')}"
            )

        # 2. Maksimal 3 oy oldinga (12+3=15 xatosini bermaydi)
        # timedelta(days=90) har qanday oyda xatosiz ishlaydi
        max_date = today + timedelta(days=90)

        if appointment_date > max_date:
            raise ValidationError(
                f"Qabul sanasi juda uzoq muddatga belgilandi. "
                f"Maksimal {max_date.strftime('%d.%m.%Y')} gacha bo'lishi mumkin"
            )

        return appointment_date


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


class ContactForm(forms.ModelForm):
    """Bog'lanish formasi"""

    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998XXXXXXXXX'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Xabar mavzusi'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Xabaringiz...'}),
        }

        labels = {
            'name': 'Ism',
            'phone': 'Telefon',
            'subject': 'Mavzu',
            'message': 'Xabar'
        }

        help_texts = {
            'phone': 'Telefon raqamingizni +998XXXXXXXXX formatida kiriting',
            'message': 'Kamida 13 ta belgi kiriting',
        }

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

        if len(message) < 10:
            raise ValidationError(
                f"Xabar juda qisqa. Kamida 10 ta belgi kiriting. "
                f"Hozir: {len(message)} ta belgi"
            )

        if len(message) > 5000:
            raise ValidationError(
                f"Xabar juda uzun (maksimal 5000 ta belgi). "
                f"Hozir: {len(message)} ta belgi"
            )

        return message

    def clean_phone(self):
        """Telefon raqami validatsiyasi"""
        phone = self.cleaned_data.get('phone')
        # forms.py oxirida validate_uzbek_phone bor, shundan foydalanamiz
        return validate_uzbek_phone(phone)


def validate_uzbek_phone(phone: str) -> str:
    """
    O'zbekiston telefon raqamini tekshirish.
    Returns: Formatlangan telefon (+998XXXXXXXXX) yoki ValidationError.
    """

    if not phone:
        raise ValidationError("Telefon raqam majburiy maydon")

    # Bo'sh joylar va maxsus belgilarni olib tashlash
    phone = re.sub(r'[\s\-\(\)]', '', phone)

    if phone.startswith('++'):
        phone = phone.lstrip('+')

    pattern = r'^(?:\+?998\d{9})$'
    if not re.match(pattern, phone):
        raise ValidationError(
            "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak. Masalan: +998901234567"
        )

    # + qo'shish agar yo'q bo'lsa
    if not phone.startswith('+'):
        phone = '+' + phone

    return phone