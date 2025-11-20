# from .models import SiteSettings, Department, Service
# from django.core.cache import cache
#
#
# def site_settings(request):
#     """
#     Barcha sahifalarda sayt sozlamalarini ko'rsatish
#     """
#     # Keshdan olish (15 daqiqa)
#     settings = cache.get('site_settings')
#
#     if not settings:
#         try:
#             settings = SiteSettings.objects.first()
#             cache.set('site_settings', settings, 60 * 15)  # 15 daqiqa
#         except:
#             settings = None
#
#     # Departments va Services ham barcha sahifalarda kerak
#     departments = cache.get('header_departments')
#     if not departments:
#         departments = Department.objects.filter(is_active=True).only(
#             'id', 'name_uz', 'name_ru', 'name_en', 'icon'
#         )[:10]
#         cache.set('header_departments', departments, 60 * 15)
#
#     services = cache.get('header_services')
#     if not services:
#         services = Service.objects.filter(is_active=True).select_related('department').only(
#             'id', 'name_uz', 'name_ru', 'name_en', 'price', 'department__name_uz'
#         )[:10]
#         cache.set('header_services', services, 60 * 15)
#
#     return {
#         'site_settings': settings,
#         'departments': departments,
#         'services': services,
#     }


from .models import SiteSettings, Department, Service
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


def site_settings(request):
    """
    ✅ FIXED: Optimized context processor with proper caching
    Barcha sahifalarda sayt sozlamalarini ko'rsatish
    """

    def get_cached_site_settings():
        """SiteSettings ni cache'dan olish yoki yangilash"""
        cache_key = 'site_settings_v2'  # Version qo'shildi
        settings_obj = cache.get(cache_key)

        if settings_obj is None:
            try:
                settings_obj = SiteSettings.objects.first()
                if settings_obj:
                    cache.set(cache_key, settings_obj, 60 * 60)  # 1 soat
            except Exception as e:
                logger.error(f"Error loading site settings: {str(e)}")
                settings_obj = None

        return settings_obj

    def get_cached_departments():
        """Departments ni cache'dan olish"""
        cache_key = 'header_departments_v2'
        departments = cache.get(cache_key)

        if departments is None:
            try:
                # ✅ FIXED: list() bilan caching
                departments = list(
                    Department.objects.filter(is_active=True)
                    .only('id', 'name_uz', 'name_ru', 'name_en', 'icon', 'slug')
                    .order_by('order')[:10]
                )
                cache.set(cache_key, departments, 60 * 15)  # 15 daqiqa
            except Exception as e:
                logger.error(f"Error loading departments: {str(e)}")
                departments = []

        return departments

    def get_cached_services():
        """Services ni cache'dan olish"""
        cache_key = 'header_services_v2'
        services = cache.get(cache_key)

        if services is None:
            try:
                # ✅ FIXED: select_related va only() bilan
                services = list(
                    Service.objects.filter(is_active=True)
                    .select_related('department')
                    .only(
                        'id', 'name_uz', 'name_ru', 'name_en',
                        'slug', 'price', 'icon',
                        'department__name_uz', 'department__slug'
                    )
                    .order_by('order')[:10]
                )
                cache.set(cache_key, services, 60 * 15)  # 15 daqiqa
            except Exception as e:
                logger.error(f"Error loading services: {str(e)}")
                services = []

        return services

    # Barcha ma'lumotlarni olish
    try:
        return {
            'site_settings': get_cached_site_settings(),
            'departments': get_cached_departments(),
            'services': get_cached_services(),
        }
    except Exception as e:
        logger.error(f"Context processor error: {str(e)}")
        return {
            'site_settings': None,
            'departments': [],
            'services': [],
        }


def clear_site_cache():
    """
    ✅ ADDED: Cache ni tozalash uchun utility function
    Admin panel'dan chaqirish mumkin
    """
    cache_keys = [
        'site_settings_v2',
        'header_departments_v2',
        'header_services_v2',
    ]

    for key in cache_keys:
        cache.delete(key)

    logger.info("Site cache cleared successfully")