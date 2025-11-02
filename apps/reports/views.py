# apps/reports/views.py
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate, TruncHour
from datetime import datetime
from apps.detections.models import Detection


def reports(request):
    """Advanced reports with trends, breakdowns, anomalies, and extra analytics."""

    mode = request.GET.get("mode", "range")  # default: range
    now = timezone.now()
    start, end = None, None

    # -------------------
    # FILTERING
    # -------------------
    if mode == "range":
        start_str, end_str = request.GET.get("start_date"), request.GET.get("end_date")
        try:
            start_dt = (
                datetime.strptime(start_str, "%Y-%m-%d")
                if start_str else now - timezone.timedelta(days=30)
            )
            end_dt = (
                datetime.strptime(end_str, "%Y-%m-%d")
                if end_str else now
            )
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        except Exception:
            start_dt = now - timezone.timedelta(days=30)
            end_dt = now

        # ✅ Safe timezone handling
        start = make_aware(start_dt) if is_naive(start_dt) else start_dt
        end = make_aware(end_dt) if is_naive(end_dt) else end_dt

    elif mode == "month_day":
        year_str, month_str, day_str = (
            request.GET.get("year"),
            request.GET.get("month"),
            request.GET.get("day"),
        )
        try:
            year = int(year_str) if year_str else now.year
            month = int(month_str) if month_str else now.month
            if day_str:
                day = int(day_str)
                start_dt = datetime(year, month, day, 0, 0, 0)
                end_dt = datetime(year, month, day, 23, 59, 59)
            else:
                start_dt = datetime(year, month, 1, 0, 0, 0)
                if month == 12:
                    end_dt = datetime(year, 12, 31, 23, 59, 59)
                else:
                    next_month = datetime(year, month + 1, 1)
                    end_dt = next_month - timezone.timedelta(seconds=1)
        except Exception:
            start_dt = now - timezone.timedelta(days=1)
            end_dt = now

        # ✅ Safe timezone handling
        start = make_aware(start_dt) if is_naive(start_dt) else start_dt
        end = make_aware(end_dt) if is_naive(end_dt) else end_dt

    else:  # fallback quick
        start = now - timezone.timedelta(days=1)
        end = now

    # -------------------
    # QUERIES
    # -------------------
    detections_qs = Detection.objects.filter(detected_at__gte=start, detected_at__lte=end)

    totals = detections_qs.aggregate(
        total_revenue=Sum("toll_rate"),
        total_vehicles=Count("id")
    )

    all_vehicle_types = [v[0] for v in Detection.VEHICLE_CHOICES]

    # Initialize by_type with all vehicle types
    by_type_dict = {
        vt: {'vehicle_type': vt, 'count': 0, 'revenue': 0}
        for vt in all_vehicle_types
    }

    # Get data from the database
    by_type_qs = (
        detections_qs.values("vehicle_type")
        .annotate(count=Count("id"), revenue=Sum("toll_rate"))
    )

    # Update the dictionary with actual data
    for row in by_type_qs:
        if row['vehicle_type'] in by_type_dict:
            by_type_dict[row['vehicle_type']] = row

    # Convert the dictionary to a list and sort it
    by_type = sorted(list(by_type_dict.values()), key=lambda x: x['vehicle_type'])

    by_day = list(
        detections_qs.annotate(day=TruncDate("detected_at"))
        .values("day")
        .annotate(vehicles=Count("id"), revenue=Sum("toll_rate"))
        .order_by("day")
    )

    by_hour = list(
        detections_qs.annotate(hour=TruncHour("detected_at"))
        .values("hour")
        .annotate(vehicles=Count("id"))
        .order_by("hour")
    )

    top_type = (
        detections_qs.values("vehicle_type")
        .annotate(count=Count("id"))
        .order_by("-count")
        .first()
    )

    busiest_day = (
        detections_qs.annotate(day=TruncDate("detected_at"))
        .values("day")
        .annotate(vehicles=Count("id"))
        .order_by("-vehicles")
        .first()
    )

    busiest_hour = (
        detections_qs.annotate(hour=TruncHour("detected_at"))
        .values("hour")
        .annotate(vehicles=Count("id"))
        .order_by("-vehicles")
        .first()
    )

    avg_revenue_per_vehicle = 0
    if totals.get("total_vehicles"):
        avg_revenue_per_vehicle = round(
            (totals.get("total_revenue") or 0) / totals.get("total_vehicles"), 2
        )

    anomalies = list(detections_qs.filter(toll_rate__lte=0).values()[:50])

    context = {
        "totals": {
            "revenue": totals.get("total_revenue") or 0,
            "vehicles": totals.get("total_vehicles") or 0,
        },
        "by_type": by_type,
        "by_day": by_day,
        "by_hour": by_hour,
        "top_type": top_type,
        "busiest_day": busiest_day,
        "busiest_hour": busiest_hour,
        "avg_revenue_per_vehicle": avg_revenue_per_vehicle,
        "anomalies": anomalies,
        "detections": detections_qs.order_by("-detected_at")[:300],
        "start": start,
        "end": end,
        "selected": {
            "start_date": request.GET.get("start_date", ""),
            "end_date": request.GET.get("end_date", ""),
        },
    }
    return render(request, "dashbaord/admin/report.html", context)
