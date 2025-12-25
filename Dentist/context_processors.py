from .models import SiteSettings, Department, WorkingHours


def site_settings(request):
    """
    Faqat barcha sahifalar uchun umumiy bo'lgan
    ma'lumotlarni (Settings, Footer xizmatlari) taqdim etadi.
    """
    try:
        # Sayt sozlamalari (Logo, Manzil va h.k.)
        settings = SiteSettings.objects.first()

        # Footerda chiqishi kerak bo'lgan xizmatlar ro'yxati
        # Bu siz qo'shgan "Tish davolash"ni ko'rsatadi
        departments_list = Department.objects.filter(is_active=True).only('name', 'slug')[:5]

        # Footer uchun ish vaqti
        working_hours = WorkingHours.objects.all().order_by('day')
    except Exception:
        settings = None
        departments_list = []
        working_hours = []

    return {
        'settings': settings,
        'departments_list': departments_list,
        'working_hours': working_hours,
    }