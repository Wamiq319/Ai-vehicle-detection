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


from apps.detections.models import Detection
from apps.tolls.models import TollRate
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

@login_required
def dashboard_view(request):
    """Dashboard page with overall system stats."""
    
    # Overall stats
    total_vehicles = Detection.objects.count()
    total_revenue = Detection.objects.aggregate(total_revenue=Sum('toll_rate'))['total_revenue'] or 0
    
    # Toll rates
    toll_rates = TollRate.objects.all()

    context = {
        'user': request.user,
        'stats': {
            'total_vehicles': total_vehicles,
            'total_revenue': total_revenue,
        },
        'toll_points': toll_rates,
    }
    return render(request, 'dashbaord/admin/dashboard.html', context)