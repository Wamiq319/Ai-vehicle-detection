from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import datetime

from apps.detections.models import Detection


def reports(request):
    """Admin reports page with filters: quick (day/week/month), month/day, and custom range."""
    mode = request.GET.get("mode", "quick")  # quick | month_day | range
    period = request.GET.get("period", "day")  # used when mode=quick

    now = timezone.now()
    start = None
    end = None

    if mode == "month_day":
        year_str = request.GET.get("year")
        month_str = request.GET.get("month")  # 1-12
        day_str = request.GET.get("day")      # 1-31 optional

        try:
            year = int(year_str) if year_str else now.year
            month = int(month_str) if month_str else now.month
            if day_str:
                day = int(day_str)
                start_dt = datetime(year, month, day, 0, 0, 0)
                end_dt = datetime(year, month, day, 23, 59, 59)
            else:
                # whole month
                start_dt = datetime(year, month, 1, 0, 0, 0)
                if month == 12:
                    end_dt = datetime(year, 12, 31, 23, 59, 59)
                else:
                    next_month = datetime(year, month + 1, 1)
                    end_dt = (next_month - timezone.timedelta(seconds=1))
        except ValueError:
            # fallback to last 24h on invalid input
            start_dt = (now - timezone.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_dt = now

        start = timezone.make_aware(start_dt) if timezone.is_naive(start_dt) else start_dt
        end = timezone.make_aware(end_dt) if timezone.is_naive(end_dt) else end_dt

    elif mode == "range":
        # Expect YYYY-MM-DD for start_date and end_date
        start_str = request.GET.get("start_date")
        end_str = request.GET.get("end_date")
        try:
            if start_str:
                s_parts = [int(p) for p in start_str.split("-")]
                start_dt = datetime(s_parts[0], s_parts[1], s_parts[2], 0, 0, 0)
            else:
                start_dt = now - timezone.timedelta(days=30)
            if end_str:
                e_parts = [int(p) for p in end_str.split("-")]
                end_dt = datetime(e_parts[0], e_parts[1], e_parts[2], 23, 59, 59)
            else:
                end_dt = now
        except Exception:
            start_dt = now - timezone.timedelta(days=30)
            end_dt = now

        start = timezone.make_aware(start_dt) if timezone.is_naive(start_dt) else start_dt
        end = timezone.make_aware(end_dt) if timezone.is_naive(end_dt) else end_dt

    else:
        # quick mode
        if period == "week":
            start = now - timezone.timedelta(days=7)
        elif period == "month":
            start = now - timezone.timedelta(days=30)
        else:
            period = "day"
            start = now - timezone.timedelta(days=1)
        end = now

    detections_qs = Detection.objects.filter(detected_at__gte=start, detected_at__lte=end)

    totals = detections_qs.aggregate(
        total_revenue=Sum("toll_rate"),
        total_vehicles=Count("id"),
    )

    by_type = list(
        detections_qs.values("vehicle_type").annotate(
            count=Count("id"),
            revenue=Sum("toll_rate"),
        ).order_by("vehicle_type")
    )

    # years list for selector
    try:
        years = [d.year for d in Detection.objects.dates("detected_at", "year")]
    except Exception:
        years = list({d.detected_at.year for d in Detection.objects.all()})
        years.sort()

    context = {
        "mode": mode,
        "period": period,
        "totals": {
            "revenue": totals.get("total_revenue") or 0,
            "vehicles": totals.get("total_vehicles") or 0,
        },
        "by_type": by_type,
        "detections": detections_qs.order_by("-detected_at")[:300],
        "start": start,
        "end": end,
        "years": years or [now.year],
        "selected": {
            "year": request.GET.get("year", str(now.year)),
            "month": request.GET.get("month", str(now.month)),
            "day": request.GET.get("day", ""),
            "start_date": request.GET.get("start_date", ""),
            "end_date": request.GET.get("end_date", ""),
        }
    }

    return render(request, "dashbaord/admin/report.html", context)

