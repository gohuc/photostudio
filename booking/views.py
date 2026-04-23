from django.shortcuts import render
from django.http import JsonResponse
from .models import BookingType, ExtraService, Booking
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from services.models import Package
import json
import traceback

def booking_page(request):
    booking_types = BookingType.objects.filter(is_active=True)
    extra_services = ExtraService.objects.filter(is_active=True)
    packages = Package.objects.filter(is_active=True) 
    
    services_by_category = {}
    for service in extra_services:
        cat = service.category if service.category else "Другие услуги"
        if cat not in services_by_category:
            services_by_category[cat] = []
        services_by_category[cat].append(service)
    
    selected_package = None
    package_slug = request.GET.get('package')
    if package_slug:
        try:
            selected_package = Package.objects.get(slug=package_slug, is_active=True)
        except Package.DoesNotExist:
            pass
    
    context = {
        'booking_types': booking_types,
        'services_by_category': services_by_category.items(),
        'packages': packages, 
        'selected_package': selected_package,  
    }
    return render(request, 'booking/booking.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def submit_booking(request):
    try:
        data = json.loads(request.body)
        
        date_str = data['date']
        time_slot = data['time']
        package_id = data.get('package_id')
        booking_type_id = data.get('booking_type_id')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time_slot, '%H:%M').time()
        except ValueError:
            return JsonResponse({'status': 'error', 'error': 'Неверный формат даты или времени'})
    
        now = datetime.now()
        if date_obj < now.date():
            return JsonResponse({'status': 'error', 'error': 'Нельзя забронировать прошедшую дату'})
        
        if date_obj == now.date():
            current_minutes = now.hour * 60 + now.minute
            slot_minutes = time_obj.hour * 60 + time_obj.minute
            if slot_minutes <= current_minutes + 30:
                return JsonResponse({'status': 'error', 'error': 'Нельзя забронировать прошедшее время'})
        
        duration = 60
        booking_type = None
        is_package = False
        package = None
        
        if package_id:
            try:
                package = Package.objects.get(id=package_id)
                duration = int(package.duration_minutes) if package.duration_minutes else 120
                is_package = True
                
                booking_type, _ = BookingType.objects.get_or_create(
                    name="Пакет услуг",
                    defaults={
                        'duration_minutes': duration,
                        'price': package.price,
                        'is_active': True
                    }
                )
                booking_type.price = package.price
                
            except Package.DoesNotExist:
                return JsonResponse({'status': 'error', 'error': 'Пакет не найден'})
        elif booking_type_id:
            try:
                booking_type = BookingType.objects.get(id=booking_type_id)
                duration = int(booking_type.duration_minutes) if booking_type.duration_minutes else 60
            except BookingType.DoesNotExist:
                return JsonResponse({'status': 'error', 'error': 'Тип бронирования не найден'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Не выбран тип или пакет'})
        
        start_minutes = time_obj.hour * 60 + time_obj.minute
        end_minutes = start_minutes + duration
        
        print(f"=== ПРОВЕРКА ПЕРЕСЕЧЕНИЯ ===")
        print(f"Новая бронь: {time_slot} длительность {duration} мин -> {start_minutes} - {end_minutes}")
        
        existing_bookings = Booking.objects.filter(
            date=date_obj,
            status__in=['new', 'confirmed']
        ).select_related('booking_type')
        
        print(f"Существующих броней: {existing_bookings.count()}")
        
        has_conflict = False
        conflict_time = None
        
        for existing in existing_bookings:
            existing_start = existing.time.hour * 60 + existing.time.minute
            
            if existing.booking_type and existing.booking_type.duration_minutes:
                existing_duration = int(existing.booking_type.duration_minutes)
            else:
                existing_duration = 60
            
            existing_end = existing_start + existing_duration
            
            print(f"  Существующая: {existing.time} длительность {existing_duration} мин -> {existing_start} - {existing_end}")
            print(f"  Проверка: {start_minutes} < {existing_end} = {start_minutes < existing_end}")
            print(f"  Проверка: {end_minutes} > {existing_start} = {end_minutes > existing_start}")
            
            if start_minutes < existing_end and end_minutes > existing_start:
                has_conflict = True
                conflict_time = existing.time.strftime('%H:%M')
                print(f"  >>> КОНФЛИКТ с {conflict_time}!")
                break
        
        if has_conflict:
            return JsonResponse({
                'status': 'error',
                'error': f'Время {time_slot} пересекается с бронью в {conflict_time}'
            })
        
        booking = Booking.objects.create(
            client_name=data['client_name'],
            client_email=data['client_email'],
            client_phone=data['client_phone'],
            booking_type=booking_type,
            date=date_obj,
            time=time_obj,
            total_price=data['total_price'],
            status='new'
        )
        
        if data.get('extra_services'):
            extra_services = ExtraService.objects.filter(id__in=data['extra_services'])
            booking.extra_services.set(extra_services)
        
        return JsonResponse({'status': 'ok', 'booking_id': booking.id})
        
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'error': str(e)})

def get_available_slots(request):
    date_str = request.GET.get('date')
    
    if not date_str:
        return JsonResponse({'slots': []})
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'slots': []})
    
    WORK_START_HOUR = 10
    WORK_END_HOUR = 22
    
    all_slots = []
    for hour in range(WORK_START_HOUR, WORK_END_HOUR):
        all_slots.append(f"{hour:02d}:00")
    
    now = datetime.now()
    is_today = (date == now.date())
    current_minutes_total = now.hour * 60 + now.minute
    
    try:
        bookings = Booking.objects.filter(
            date=date,
            status__in=['new', 'confirmed']
        ).select_related('booking_type')
        
        busy_slots = set()
        
        for booking in bookings:
            if booking.booking_type and booking.booking_type.duration_minutes:
                duration = int(booking.booking_type.duration_minutes)
            else:
                duration = 60
            
            if hasattr(booking.time, 'hour'):
                start_hour = booking.time.hour
                start_minute = booking.time.minute
            else:
                start_hour = int(str(booking.time).split(':')[0])
                start_minute = int(str(booking.time).split(':')[1])
            
            start_minutes_total = start_hour * 60 + start_minute
            end_minutes_total = start_minutes_total + duration
            
            slot_minutes = start_minutes_total
            while slot_minutes < end_minutes_total:
                slot_hour = slot_minutes // 60
                if WORK_START_HOUR <= slot_hour < WORK_END_HOUR:
                    busy_slots.add(f"{slot_hour:02d}:00")
                slot_minutes += 60
        
        available_slots = []
        for slot in all_slots:
            if slot in busy_slots:
                continue
            if is_today:
                slot_hour = int(slot.split(':')[0])
                slot_minutes_total = slot_hour * 60
                if slot_minutes_total <= current_minutes_total + 60:
                    continue
            available_slots.append(slot)
        
        print(f"Доступные слоты для {date}: {available_slots}")
        return JsonResponse({'slots': available_slots})
        
    except Exception as e:
        print(f"Ошибка в get_available_slots: {e}")
        return JsonResponse({'slots': all_slots})