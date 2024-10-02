from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from apps.shop.models import Orderdetails

@login_required
def sortie_journalier(request):
    
    today = timezone.now().date()
    start_date = today - timedelta(days=30)  # Last 30 days

    sales_data = Orderdetails.objects.filter(
        created_at__date__range=[start_date, today]
    ).select_related('order').values(
        'created_at__date',
        'order__author__username',
        'product_name',
        'quantity',
        'sub_total_ttc',
        'order__billing_address',
        'order__shipping_address'
    ).order_by('created_at__date')

    daily_sales_summary = Orderdetails.objects.filter(
        created_at__date__range=[start_date, today]
    ).values(
        'created_at__date'
    ).annotate(
        total_sales=Sum('sub_total_ttc')
    ).order_by('created_at__date')
    
    # Prepare data for the chart
    labels = [entry['created_at__date'].strftime('%Y-%m-%d') for entry in daily_sales_summary]
    data = [entry['total_sales'] for entry in daily_sales_summary]

    context = {
        'sales_data': sales_data,
        'daily_sales_summary': daily_sales_summary,
        'chart_labels': labels,
        'chart_data': data,
        'start_date': start_date,
        'end_date': today,
        'page':'stock',
        'subpage':'journalier_tab',
    }
        

    return render(request, 'servicedsi/index.html', context)