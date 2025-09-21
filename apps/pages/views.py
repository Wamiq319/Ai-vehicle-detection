from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime, timedelta



# =============================================================================
# LANDING & AUTHENTICATION VIEWS
# =============================================================================

def landing_page(request):
    """Landing page."""
    return render(request, 'landing.html')


@login_required
def dashboard_view(request):
    """Dashboard page with dummy data."""
    # Dummy data for dashboard
    context = {
        'user': request.user,
        'stats': {
            'total_vehicles_today': 1247,
            'total_revenue_today': 18750.00,
            'active_toll_points': 8,
            'detection_accuracy': 98.5,
        },
        'recent_activities': [
            {
                'time': '10:30 AM',
                'vehicle_type': 'Car',
                'toll_point': 'Highway A1',
                'amount': 50.00,
                'status': 'Paid'
            },
            {
                'time': '10:25 AM',
                'vehicle_type': 'Truck',
                'toll_point': 'Highway B2',
                'amount': 150.00,
                'status': 'Paid'
            },
            {
                'time': '10:20 AM',
                'vehicle_type': 'Bus',
                'toll_point': 'Highway A1',
                'amount': 100.00,
                'status': 'Paid'
            },
            {
                'time': '10:15 AM',
                'vehicle_type': 'Car',
                'toll_point': 'Highway C3',
                'amount': 50.00,
                'status': 'Paid'
            },
            {
                'time': '10:10 AM',
                'vehicle_type': 'Motorcycle',
                'toll_point': 'Highway A1',
                'amount': 25.00,
                'status': 'Paid'
            },
        ],
        'toll_points': [
            {'name': 'Highway A1', 'status': 'Active', 'vehicles_count': 156, 'revenue': 7800.00},
            {'name': 'Highway B2', 'status': 'Active', 'vehicles_count': 89, 'revenue': 13350.00},
            {'name': 'Highway C3', 'status': 'Active', 'vehicles_count': 203, 'revenue': 10150.00},
            {'name': 'Highway D4', 'status': 'Maintenance', 'vehicles_count': 0, 'revenue': 0.00},
        ],
        'chart_data': {
            'labels': ['6 AM', '8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM'],
            'vehicles': [45, 89, 156, 203, 178, 145, 98, 67],
            'revenue': [2250, 4450, 7800, 10150, 8900, 7250, 4900, 3350]
        }
    }
    return render(request, 'dashbaord/admin/dashboard.html', context)