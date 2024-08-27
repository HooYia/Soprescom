from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.shop.models.Order  import Order
from apps.serviceapresvente.models import Sav_request, Client_sav


@login_required
def client_sav(request):
    # Assuming there is a relationship between Customer and Client_sav
    try:
        client_sav_instance = Client_sav.objects.filter(userLog=request.user)
    except Client_sav.DoesNotExist:
        client_sav_instance = None

    # Get all the CommandeSav for the connected user if client_sav_instance exists
    if client_sav_instance:
        savs = Sav_request.objects.filter(client_sav__in=client_sav_instance)
    else:
        savs = Sav_request.objects.none()  # No results if no client_sav_instance found

    return render(request, "dashboard/index.html", {'savs': savs, 'page': 'my_savs'})
