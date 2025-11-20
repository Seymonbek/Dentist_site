# from django import forms
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _
# from django.utils import timezone
# from datetime import datetime, timedelta
# from .models import Appointment, ContactMessage
#
#
# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['name', 'phone', 'email', 'department', 'doctor', 'service', 'date', 'time', 'message']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ismingiz',
#                 'required': True
#             }),
#             'phone': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': '+998 XX XXX XX XX',
#                 'required': True,
#                 'pattern': r'^\+998\d{9}$'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email manzilingiz',
#                 'required': True
#             }),
#             'department': forms.Select(attrs={
#                 'class': 'form-control',
#                 'required': True
#             }),
#             'doctor': forms.Select(attrs={
#                 'class': 'form-control',
#             }),
#             'service': forms.Select(attrs={
#                 'class': 'form-control',
#             }),
#             'date': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'type': 'date',
#                 'required': True,
#                 'min': timezone.now().date().isoformat()
#             }),
#             'time': forms.TimeInput(attrs={
#                 'class': 'form-control',
#                 'type': 'time',
#                 'required': True,
#                 'min': '09:00',
#                 'max': '20:00'
#             }),
#             'message': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Qo\'shimcha ma\'lumot',
#                 'rows': 4
#             }),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Doctor va service fieldlarini ixtiyoriy qilish
#         self.fields['doctor'].required = False
#         self.fields['service'].required = False
#         self.fields['message'].required = False
#
#     def clean_phone(self):
#         phone = self.cleaned_data.get('phone')
#         if phone:
#             # Telefon raqamini formatini tekshirish
#             if not phone.startswith('+998'):
#                 raise ValidationError(_('Telefon raqami +998 bilan boshlanishi kerak'))
#             if len(phone) != 13:
#                 raise ValidationError(_('Telefon raqami 13 ta belgidan iborat bo\'lishi kerak'))
#         return phone
#
#     def clean_date(self):
#         date = self.cleaned_data.get('date')
#         if date:
#             # O'tmishdagi sanani tanlash mumkin emasligini tekshirish
#             today = timezone.now().date()
#             if date < today:
#                 raise ValidationError(_('O\'tmishdagi sanani tanlay olmaysiz'))
#
#             # 3 oydan keyin bo'lgan sanani tanlash mumkin emasligini tekshirish
#             max_date = today + timedelta(days=90)
#             if date > max_date:
#                 raise ValidationError(_('3 oydan keyin bo\'lgan sanani tanlay olmaysiz'))
#
#         return date
#
#     def clean_time(self):
#         time = self.cleaned_data.get('time')
#         if time:
#             # Ish vaqti tekshiruvi (09:00 - 20:00)
#             work_start = datetime.strptime('09:00', '%H:%M').time()
#             work_end = datetime.strptime('20:00', '%H:%M').time()
#
#             if time < work_start or time > work_end:
#                 raise ValidationError(_('Ish vaqti 09:00 dan 20:00 gacha'))
#
#         return time
#
#     def clean(self):
#         cleaned_data = super().clean()
#         date = cleaned_data.get('date')
#         time = cleaned_data.get('time')
#         department = cleaned_data.get('department')
#         doctor = cleaned_data.get('doctor')
#
#         # Shifokor tanlangan bo'lsa, u tanlangan bo'limda ishlashini tekshirish
#         if doctor and department:
#             if not doctor.departments.filter(id=department.id).exists():
#                 raise ValidationError({
#                     'doctor': _('Tanlangan shifokor bu bo\'limda ishlamaydi')
#                 })
#
#         # Bir xil vaqtda bitta shifokorga bir nechta qabul bo'lmasligi uchun tekshirish
#         if date and time and doctor:
#             existing_appointments = Appointment.objects.filter(
#                 date=date,
#                 time=time,
#                 doctor=doctor,
#                 status__in=['pending', 'confirmed']
#             )
#             if self.instance.pk:
#                 existing_appointments = existing_appointments.exclude(pk=self.instance.pk)
#
#             if existing_appointments.exists():
#                 raise ValidationError({
#                     'time': _('Bu vaqtda shifokor band')
#                 })
#
#         return cleaned_data
#
#
# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['name', 'email', 'subject', 'message']
#         widgets = {
#             'name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Ismingiz',
#                 'required': True
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email manzilingiz',
#                 'required': True
#             }),
#             'subject': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Mavzu',
#                 'required': True
#             }),
#             'message': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Xabaringiz',
#                 'rows': 10,
#                 'required': True
#             }),
#         }
#
#     def clean_name(self):
#         name = self.cleaned_data.get('name')
#         if name:
#             # Ismda kamida 2 ta harf bo'lishi kerak
#             if len(name.strip()) < 2:
#                 raise ValidationError(_('Ism kamida 2 ta belgidan iborat bo\'lishi kerak'))
#
#             # Ismda faqat harflar va bo'shliqlar bo'lishi kerak
#             if not all(c.isalpha() or c.isspace() for c in name):
#                 raise ValidationError(_('Ismda faqat harflar bo\'lishi kerak'))
#
#         return name
#
#     def clean_subject(self):
#         subject = self.cleaned_data.get('subject')
#         if subject:
#             # Mavzu kamida 5 ta belgidan iborat bo'lishi kerak
#             if len(subject.strip()) < 5:
#                 raise ValidationError(_('Mavzu kamida 5 ta belgidan iborat bo\'lishi kerak'))
#
#         return subject
#
#     def clean_message(self):
#         message = self.cleaned_data.get('message')
#         if message:
#             # Xabar kamida 10 ta belgidan iborat bo'lishi kerak
#             if len(message.strip()) < 10:
#                 raise ValidationError(_('Xabar kamida 10 ta belgidan iborat bo\'lishi kerak'))
#
#             # Xabar ko'pi bilan 2000 ta belgidan iborat bo'lishi kerak
#             if len(message.strip()) > 2000:
#                 raise ValidationError(_('Xabar ko\'pi bilan 2000 ta belgidan iborat bo\'lishi kerak'))
#
#         return message


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, timedelta
import re
from .models import Appointment, ContactMessage


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'phone', 'email', 'department', 'doctor', 'service', 'date', 'time', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingiz',
                'required': True,
                'minlength': 2,
                'maxlength': 100
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 XX XXX XX XX',
                'required': True,
                'pattern': r'^\+998\d{9}$'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzilingiz',
                'required': True
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'doctor': forms.Select(attrs={
                'class': 'form-control',
            }),
            'service': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'min': timezone.now().date().isoformat()
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True,
                'min': '09:00',
                'max': '20:00',
                'step': '900'  # 15 daqiqa qadamlari
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Qo\'shimcha ma\'lumot',
                'rows': 4,
                'maxlength': 1000
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Doctor va service fieldlarini ixtiyoriy qilish
        self.fields['doctor'].required = False
        self.fields['service'].required = False
        self.fields['message'].required = False

        # Empty label qo'shish
        self.fields['department'].empty_label = _("Bo'limni tanlang")
        self.fields['doctor'].empty_label = _("Shifokorni tanlang (ixtiyoriy)")
        self.fields['service'].empty_label = _("Xizmatni tanlang (ixtiyoriy)")

    def clean_name(self):
        """✅ FIXED: Ism validatsiyasi"""
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError(_('Ism kiritilishi shart'))

        if len(name) < 2:
            raise ValidationError(_('Ism kamida 2 ta belgidan iborat bo\'lishi kerak'))

        if len(name) > 100:
            raise ValidationError(_('Ism juda uzun'))

        # Faqat harflar va bo'shliq
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁўЎқҚғҒҳҲ\s\'-]+$', name, re.UNICODE):
            raise ValidationError(_('Ismda faqat harflar bo\'lishi mumkin'))

        return name

    def clean_phone(self):
        """✅ FIXED: Telefon validatsiyasi"""
        phone = self.cleaned_data.get('phone', '').strip()

        if not phone:
            raise ValidationError(_('Telefon raqami kiritilishi shart'))

        # Bo'sh joylarni olib tashlash
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # +998 bilan boshlanishi kerak
        if not phone.startswith('+998'):
            raise ValidationError(_('Telefon raqami +998 bilan boshlanishi kerak'))

        # Uzunlik tekshiruvi
        if len(phone) != 13:  # +998XXXXXXXXX
            raise ValidationError(_('Telefon raqami noto\'g\'ri formatda'))

        # Regex pattern bilan tekshirish
        phone_pattern = re.compile(r'^\+998(9[012345789]|6[125679]|7[01234569])\d{7}$')
        if not phone_pattern.match(phone):
            raise ValidationError(_('Telefon raqami noto\'g\'ri formatda'))

        return phone

    def clean_email(self):
        """✅ FIXED: Email validatsiyasi"""
        email = self.cleaned_data.get('email', '').strip().lower()

        if not email:
            raise ValidationError(_('Email kiritilishi shart'))

        # Email pattern
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValidationError(_('Email noto\'g\'ri formatda'))

        return email

    def clean_date(self):
        """✅ FIXED: Sana validatsiyasi"""
        date = self.cleaned_data.get('date')

        if not date:
            raise ValidationError(_('Sana tanlanishi shart'))

        today = timezone.now().date()

        # O'tmishdagi sanani tanlash mumkin emas
        if date < today:
            raise ValidationError(_('O\'tmishdagi sanani tanlay olmaysiz'))

        # Bugundan 3 oydan keyin
        max_date = today + timedelta(days=90)
        if date > max_date:
            raise ValidationError(_('3 oydan keyin bo\'lgan sanani tanlay olmaysiz'))

        # Yakshanba kunini tekshirish (0 = Monday, 6 = Sunday)
        if date.weekday() == 6:
            raise ValidationError(_('Yakshanba kuni ish yo\'q'))

        return date

    def clean_time(self):
        """✅ FIXED: Vaqt validatsiyasi"""
        time = self.cleaned_data.get('time')

        if not time:
            raise ValidationError(_('Vaqt tanlanishi shart'))

        # Ish vaqti: 09:00 - 20:00
        work_start = datetime.strptime('09:00', '%H:%M').time()
        work_end = datetime.strptime('20:00', '%H:%M').time()

        if time < work_start or time > work_end:
            raise ValidationError(_('Ish vaqti 09:00 dan 20:00 gacha'))

        # Tushlik vaqti: 13:00 - 14:00
        lunch_start = datetime.strptime('13:00', '%H:%M').time()
        lunch_end = datetime.strptime('14:00', '%H:%M').time()

        if lunch_start <= time < lunch_end:
            raise ValidationError(_('Tushlik vaqti. 14:00 dan keyin tanlang'))

        # 15 daqiqa intervalda bo'lishi kerak (09:00, 09:15, 09:30...)
        if time.minute % 15 != 0:
            raise ValidationError(_('Vaqt 15 daqiqa oraliqda bo\'lishi kerak'))

        return time

    def clean_message(self):
        """✅ FIXED: Xabar validatsiyasi"""
        message = self.cleaned_data.get('message', '').strip()

        if message and len(message) > 1000:
            raise ValidationError(_('Xabar juda uzun (maksimal 1000 belgi)'))

        return message

    def clean(self):
        """✅ FIXED: Umumiy validatsiya"""
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        department = cleaned_data.get('department')
        doctor = cleaned_data.get('doctor')
        service = cleaned_data.get('service')

        # Shifokor tanlangan bo'lsa, u tanlangan bo'limda ishlashi kerak
        if doctor and department:
            if not doctor.departments.filter(id=department.id).exists():
                raise ValidationError({
                    'doctor': _('Tanlangan shifokor bu bo\'limda ishlamaydi')
                })

        # Xizmat tanlangan bo'lsa, u tanlangan bo'limga tegishli bo'lishi kerak
        if service and department:
            if service.department_id != department.id:
                raise ValidationError({
                    'service': _('Tanlangan xizmat bu bo\'limga tegishli emas')
                })

        # Bir xil vaqtda bitta shifokorga bir nechta qabul bo'lmasligi
        if date and time and doctor:
            # Mavjud qabullarni tekshirish
            existing = Appointment.objects.filter(
                date=date,
                time=time,
                doctor=doctor,
                status__in=['pending', 'confirmed']
            )

            # Agar edit bo'lsa, o'zini exclude qilish
            if self.instance and self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise ValidationError({
                    'time': _('Bu vaqtda shifokor band. Boshqa vaqt tanlang')
                })

        # Bugungi kun bo'lsa, o'tgan vaqtni tanlash mumkin emas
        if date and time and date == timezone.now().date():
            now = timezone.now().time()
            if time <= now:
                raise ValidationError({
                    'time': _('O\'tgan vaqtni tanlay olmaysiz')
                })

        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingiz',
                'required': True,
                'minlength': 2,
                'maxlength': 100
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzilingiz',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mavzu',
                'required': True,
                'minlength': 5,
                'maxlength': 200
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Xabaringiz',
                'rows': 10,
                'required': True,
                'minlength': 10,
                'maxlength': 2000
            }),
        }

    def clean_name(self):
        """✅ FIXED: Ism validatsiyasi"""
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError(_('Ism kiritilishi shart'))

        if len(name) < 2:
            raise ValidationError(_('Ism kamida 2 ta belgidan iborat bo\'lishi kerak'))

        if len(name) > 100:
            raise ValidationError(_('Ism juda uzun'))

        # Faqat harflar va bo'shliq
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁўЎқҚғҒҳҲ\s\'-]+$', name, re.UNICODE):
            raise ValidationError(_('Ismda faqat harflar bo\'lishi mumkin'))

        return name

    def clean_email(self):
        """✅ FIXED: Email validatsiyasi"""
        email = self.cleaned_data.get('email', '').strip().lower()

        if not email:
            raise ValidationError(_('Email kiritilishi shart'))

        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValidationError(_('Email noto\'g\'ri formatda'))

        return email

    def clean_subject(self):
        """✅ FIXED: Mavzu validatsiyasi"""
        subject = self.cleaned_data.get('subject', '').strip()

        if not subject:
            raise ValidationError(_('Mavzu kiritilishi shart'))

        if len(subject) < 5:
            raise ValidationError(_('Mavzu kamida 5 ta belgidan iborat bo\'lishi kerak'))

        if len(subject) > 200:
            raise ValidationError(_('Mavzu juda uzun'))

        return subject

    def clean_message(self):
        """✅ FIXED: Xabar validatsiyasi"""
        message = self.cleaned_data.get('message', '').strip()

        if not message:
            raise ValidationError(_('Xabar kiritilishi shart'))

        if len(message) < 10:
            raise ValidationError(_('Xabar kamida 10 ta belgidan iborat bo\'lishi kerak'))

        if len(message) > 2000:
            raise ValidationError(_('Xabar juda uzun (maksimal 2000 belgi)'))

        # Spam tekshiruvi - juda ko'p link
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = url_pattern.findall(message)
        if len(urls) > 3:
            raise ValidationError(_('Xabarda juda ko\'p havolalar bor'))

        return message