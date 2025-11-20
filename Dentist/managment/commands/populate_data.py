# Dentist/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from Dentist.models import (
    Department, Service, Doctor, Testimonial,
    FAQ, SiteSettings, Statistic
)


class Command(BaseCommand):
    help = 'Test ma\'lumotlarni kiritish'

    def handle(self, *args, **kwargs):
        self.stdout.write('Test ma\'lumotlarni kiritish boshlandi...')

        # 1. Site Settings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name_uz="DentaCare",
                site_name_ru="DentaCare",
                site_name_en="DentaCare",
                tagline_uz="Professional stomatologiya xizmatlari",
                tagline_ru="Профессиональные стоматологические услуги",
                tagline_en="Professional dental services",
                about_uz="DentaCare - Toshkentdagi eng yaxshi stomatologiya klinikasi. Biz 2010 yildan beri mijozlarimizga yuqori sifatli xizmat ko'rsatib kelamiz.",
                about_ru="DentaCare - лучшая стоматологическая клиника в Ташкенте. Мы предоставляем высококачественные услуги нашим клиентам с 2010 года.",
                about_en="DentaCare - the best dental clinic in Tashkent. We have been providing high quality services to our clients since 2010.",
                address_uz="Toshkent shahri, Mirzo Ulug'bek tumani, Buyuk Ipak Yo'li ko'chasi 123",
                address_ru="Ташкент, район Мирзо Улугбек, улица Великий Шелковый Путь 123",
                address_en="Tashkent city, Mirzo Ulugbek district, Great Silk Road street 123",
                phone_1="+998 71 123 45 67",
                phone_2="+998 90 123 45 67",
                email="info@dentacare.uz",
                working_hours_uz="Dushanba-Shanba: 09:00 - 20:00, Yakshanba: 10:00 - 18:00",
                working_hours_ru="Понедельник-Суббота: 09:00 - 20:00, Воскресенье: 10:00 - 18:00",
                working_hours_en="Monday-Saturday: 09:00 - 20:00, Sunday: 10:00 - 18:00",
                facebook="https://facebook.com/dentacare",
                instagram="https://instagram.com/dentacare",
                meta_description_uz="DentaCare - professional stomatologiya klinikasi. Implantatsiya, ortodontiya, terapiya.",
                meta_description_ru="DentaCare - профессиональная стоматологическая клиника. Имплантация, ортодонтия, терапия.",
                meta_description_en="DentaCare - professional dental clinic. Implantation, orthodontics, therapy.",
                meta_keywords_uz="stomatologiya, tish shifokori, implantatsiya, ortodontiya, toshkent",
                meta_keywords_ru="стоматология, стоматолог, имплантация, ортодонтия, ташкент",
                meta_keywords_en="dentistry, dentist, implantation, orthodontics, tashkent",
            )
            self.stdout.write(self.style.SUCCESS('✓ Site settings yaratildi'))

        # 2. Statistics
        stats_data = [
            {"label_uz": "Yillik tajriba", "label_ru": "Лет опыта", "label_en": "Years of Experience", "value": 15,
             "icon": "bi bi-award"},
            {"label_uz": "Baxtli bemorlar", "label_ru": "Довольных пациентов", "label_en": "Happy Patients",
             "value": 5000, "icon": "bi bi-people"},
            {"label_uz": "Shifokorlar", "label_ru": "Врачей", "label_en": "Doctors", "value": 12,
             "icon": "bi bi-hospital"},
            {"label_uz": "24/7 Xizmat", "label_ru": "24/7 Сервис", "label_en": "24/7 Service", "value": 24,
             "icon": "bi bi-clock"},
        ]
        for idx, stat in enumerate(stats_data):
            Statistic.objects.get_or_create(
                label_uz=stat["label_uz"],
                defaults={**stat, "order": idx}
            )
        self.stdout.write(self.style.SUCCESS('✓ Statistikalar yaratildi'))

        # 3. Departments
        departments_data = [
            {
                "name_uz": "Terapevtik stomatologiya",
                "name_ru": "Терапевтическая стоматология",
                "name_en": "Therapeutic Dentistry",
                "description_uz": "Tishlarni davolash, plombalar qo'yish, kanal tozalash va boshqa terapevtik xizmatlar.",
                "description_ru": "Лечение зубов, пломбирование, чистка каналов и другие терапевтические услуги.",
                "description_en": "Tooth treatment, fillings, canal cleaning and other therapeutic services.",
                "icon": "bi bi-heart-pulse",
            },
            {
                "name_uz": "Xirurgik stomatologiya",
                "name_ru": "Хирургическая стоматология",
                "name_en": "Surgical Dentistry",
                "description_uz": "Tishlarni olib tashlash, implantatsiya tayyorlash va boshqa xirurgik amaliyotlar.",
                "description_ru": "Удаление зубов, подготовка к имплантации и другие хирургические операции.",
                "description_en": "Tooth extraction, implant preparation and other surgical procedures.",
                "icon": "bi bi-scissors",
            },
            {
                "name_uz": "Ortodontiya",
                "name_ru": "Ортодонтия",
                "name_en": "Orthodontics",
                "description_uz": "Tishlarni to'g'irlash, breket sistemalar o'rnatish va tishlar holatini tuzatish.",
                "description_ru": "Выравнивание зубов, установка брекет-систем и исправление прикуса.",
                "description_en": "Teeth straightening, bracket system installation and bite correction.",
                "icon": "bi bi-align-center",
            },
            {
                "name_uz": "Implantologiya",
                "name_ru": "Имплантология",
                "name_en": "Implantology",
                "description_uz": "Yo'qolgan tishlar o'rniga implantlar o'rnatish, zamonaviy usullar.",
                "description_ru": "Установка имплантов вместо утерянных зубов, современные методы.",
                "description_en": "Installing implants to replace lost teeth, modern methods.",
                "icon": "bi bi-tools",
            },
            {
                "name_uz": "Estetik stomatologiya",
                "name_ru": "Эстетическая стоматология",
                "name_en": "Aesthetic Dentistry",
                "description_uz": "Tishlarni oqartirish, vinirlar o'rnatish, tabassum dizayni.",
                "description_ru": "Отбеливание зубов, установка виниров, дизайн улыбки.",
                "description_en": "Teeth whitening, veneer installation, smile design.",
                "icon": "bi bi-star",
            },
            {
                "name_uz": "Profilaktika",
                "name_ru": "Профилактика",
                "name_en": "Prevention",
                "description_uz": "Professional tozalash, ftorlashtirish, og'iz bo'shlig'i gigiyenasi.",
                "description_ru": "Профессиональная чистка, фторирование, гигиена полости рта.",
                "description_en": "Professional cleaning, fluoridation, oral hygiene.",
                "icon": "bi bi-shield-check",
            },
        ]

        for idx, dept in enumerate(departments_data):
            Department.objects.get_or_create(
                name_uz=dept["name_uz"],
                defaults={**dept, "order": idx}
            )
        self.stdout.write(self.style.SUCCESS('✓ Bo\'limlar yaratildi'))

        # 4. Services (har bir bo'lim uchun)
        departments = Department.objects.all()
        for dept in departments:
            for i in range(1, 4):
                Service.objects.get_or_create(
                    department=dept,
                    name_uz=f"{dept.name_uz} - Xizmat {i}",
                    defaults={
                        "name_ru": f"{dept.name_ru} - Услуга {i}",
                        "name_en": f"{dept.name_en} - Service {i}",
                        "short_description_uz": f"{dept.name_uz} bo'limidagi xizmat",
                        "short_description_ru": f"Услуга в отделении {dept.name_ru}",
                        "short_description_en": f"Service in {dept.name_en} department",
                        "description_uz": f"Bu {dept.name_uz} bo'limidagi professional xizmat. Yuqori malakali shifokorlar tomonidan amalga oshiriladi.",
                        "description_ru": f"Это профессиональная услуга в отделении {dept.name_ru}. Выполняется высококвалифицированными врачами.",
                        "description_en": f"This is a professional service in the {dept.name_en} department. Performed by highly qualified doctors.",
                        "price": 150000 + (i * 50000),
                        "duration": 30 + (i * 15),
                        "order": i,
                    }
                )
        self.stdout.write(self.style.SUCCESS('✓ Xizmatlar yaratildi'))

        # 5. FAQ
        faqs_data = [
            {
                "question_uz": "Qabulga qanday yozilsam bo'ladi?",
                "question_ru": "Как записаться на прием?",
                "question_en": "How can I make an appointment?",
                "answer_uz": "Saytdagi forma orqali, telefon qo'ng'irog'i orqali yoki bevosita klinikaga tashrif buyurib yozilishingiz mumkin.",
                "answer_ru": "Вы можете записаться через форму на сайте, по телефону или посетив клинику лично.",
                "answer_en": "You can make an appointment through the form on the website, by phone or by visiting the clinic in person.",
            },
            {
                "question_uz": "To'lovni qanday amalga oshirsam bo'ladi?",
                "question_ru": "Как я могу оплатить?",
                "question_en": "How can I pay?",
                "answer_uz": "Naqd pul, plastik karta va bank o'tkazmasi orqali to'lash mumkin.",
                "answer_ru": "Можно оплатить наличными, картой и банковским переводом.",
                "answer_en": "You can pay by cash, card and bank transfer.",
            },
            {
                "question_uz": "Birinchi konsultatsiya bepulmi?",
                "question_ru": "Первая консультация бесплатна?",
                "question_en": "Is the first consultation free?",
                "answer_uz": "Ha, birinchi konsultatsiya va ko'rik mutlaqo bepul.",
                "answer_ru": "Да, первая консультация и осмотр абсолютно бесплатны.",
                "answer_en": "Yes, the first consultation and examination are absolutely free.",
            },
        ]

        for idx, faq in enumerate(faqs_data):
            FAQ.objects.get_or_create(
                question_uz=faq["question_uz"],
                defaults={**faq, "order": idx}
            )
        self.stdout.write(self.style.SUCCESS('✓ FAQ yaratildi'))

        # 6. Testimonials
        testimonials_data = [
            {
                "name": "Aziza Karimova",
                "position_uz": "Mijoz",
                "position_ru": "Клиент",
                "position_en": "Client",
                "text_uz": "DentaCare klinikasida davolanishdan juda mamnunman. Shifokorlar juda professional va mehribon. Tavsiya qilaman!",
                "text_ru": "Очень довольна лечением в клинике DentaCare. Врачи очень профессиональные и внимательные. Рекомендую!",
                "text_en": "Very satisfied with the treatment at DentaCare clinic. The doctors are very professional and attentive. I recommend!",
                "rating": 5,
            },
            {
                "name": "Sardor Alimov",
                "position_uz": "Biznesmen",
                "position_ru": "Бизнесмен",
                "position_en": "Businessman",
                "text_uz": "Implantatsiya qildirdim, juda yaxshi natija. Hech qanday og'riq yoki noqulaylik bo'lmadi.",
                "text_ru": "Сделал имплантацию, очень хороший результат. Не было никакой боли или дискомфорта.",
                "text_en": "Had an implant done, very good result. There was no pain or discomfort.",
                "rating": 5,
            },
            {
                "name": "Malika Yusupova",
                "position_uz": "O'qituvchi",
                "position_ru": "Учитель",
                "position_en": "Teacher",
                "text_uz": "Tishlarimni oqartirdim, natija ajoyib! Klinika juda toza va zamonaviy jihozlar bilan ta'minlangan.",
                "text_ru": "Отбелила зубы, результат потрясающий! Клиника очень чистая и оснащена современным оборудованием.",
                "text_en": "Whitened my teeth, the result is amazing! The clinic is very clean and equipped with modern equipment.",
                "rating": 5,
            },
        ]

        for testimonial in testimonials_data:
            Testimonial.objects.get_or_create(
                name=testimonial["name"],
                defaults=testimonial
            )
        self.stdout.write(self.style.SUCCESS('✓ Testimonials yaratildi'))

        self.stdout.write(self.style.SUCCESS('\n=== Test ma\'lumotlar muvaffaqiyatli kiritildi! ==='))
        self.stdout.write(self.style.WARNING('\nKeyingi qadamlar:'))
        self.stdout.write('1. Admin panel uchun superuser yarating: python manage.py createsuperuser')
        self.stdout.write('2. Admin panelga kiring va shifokorlar qo\'shing')
        self.stdout.write('3. Galereya rasmlari yuklang')
        self.stdout.write('4. Saytni tekshiring: python manage.py runserver')