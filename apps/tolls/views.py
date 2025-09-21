from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TollRate

def toll_rates_view(request):
    # Fetch all rates, create default if not exist
    vehicle_types = ['truck', 'car', 'bolan']
    default_rates = {'truck': 150.00, 'car': 50.00, 'bolan': 75.00}
    rates = {}
    
    for v in vehicle_types:
        obj, created = TollRate.objects.get_or_create(
            vehicle_type=v, 
            defaults={'rate': default_rates[v]}
        )
        rates[v] = obj.rate

    if request.method == "POST":
        try:
            for v in vehicle_types:
                rate_value = request.POST.get(f"{v}_rate")
                obj = TollRate.objects.get(vehicle_type=v)
                obj.rate = float(rate_value)
                obj.save()
            messages.success(request, "Toll rates updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating rates: {str(e)}")
        return redirect('tolls:toll_rates')

    return render(request, 'dashbaord/admin/toll_rates.html', {'rates': rates})
