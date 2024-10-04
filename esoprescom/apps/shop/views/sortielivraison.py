from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from apps.serviceapresvente.models import Client_sav
from apps.shop.models.Product import ActionLog
from ..forms.SortieLivraisonFrom import SortieLivraisonForm
from ..models.SortieLivraison import SortieLivraison
from django.db import IntegrityError, transaction
from django.contrib import messages

@login_required
def create_sortie_livraison(request):
    # Fetch all SortieLivraison instances to display in the template
    sortielivraison_list = SortieLivraison.objects.filter(is_deleted=False)
    clients = Client_sav.objects.all()

    if request.method == 'POST':
        form = SortieLivraisonForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Ensure all or nothing in the database
                    form.save()
                    
                    ActionLog.objects.create(
                        product_name=form.cleaned_data['reference'],
                        action_done_by=request.user.username,
                        date_created=timezone.now(),  # Store the current timestamp as date_created
                        type = 'Sortie Livraison',
            
                    )
                messages.success(request, 'Sortie Livraison created successfully!')
                return redirect('serviceapresvente:create_sortie_livraison')
            except Exception as e:
                messages.error(request, f'Error creating Sortie Livraison: {str(e)}')
    else:
        form = SortieLivraisonForm()

    return render(
        request, 
        'servicedsi/index.html', 
        {
            'form': form, 
            'clients': clients,
            'page': 'stock',
            'subpage': 'sortie_livraison_tab',
            'sortielivraison_list': sortielivraison_list  # Pass the list to the template
        }
    )
    
@login_required
def update_sortie_livraison(request, id):
    # Fetch the specific instance of SortieLivraison based on the given id
    livraison = get_object_or_404(SortieLivraison, id=id)
    form = SortieLivraisonForm()
    
    sortielivraison_list = SortieLivraison.objects.filter(is_deleted=False)

    if request.method == 'POST':
        print(request.POST)
        try:
            with transaction.atomic():  # Begin a database transaction
                # Retrieve form data from request.POST
                livraison.date = request.POST.get('date')
                livraison.ol = request.POST.get('ol')
                livraison.ccial = request.POST.get('ccial')
                livraison.fact = request.POST.get('fact')
                livraison.bdc = request.POST.get('bdc')
                client_id = request.POST.get('client')
                
                # Ensure the client exists
                livraison.client = get_object_or_404(Client_sav, idclient=client_id)
                
                livraison.reference = request.POST.get('reference')
                livraison.serial_number = request.POST.get('serial_number')
                livraison.nature = request.POST.get('nature')
                livraison.designation = request.POST.get('designation')
                livraison.qte_dde = int(request.POST.get('qte_dde'))  # Convert to integer
                livraison.stock_initial = int(request.POST.get('stock_initial'))  # Convert to integer
                livraison.observation = request.POST.get('observation')

                # Save the updated instance to the database
                livraison.save()
                
                ActionLog.objects.create(
                        product_name=livraison.reference,
                        action_done_by=request.user.username,
                        date_modified=timezone.now(),  # Store the current timestamp as date_modified
                        type = 'Sortie Livraison',
            
                    )
                
                # Add a success message
                messages.success(request, "Sortie Livraison updated successfully.")

            # Redirect to a success page or render a response
            return redirect('serviceapresvente:create_sortie_livraison')  # Replace with your actual success URL or view

        except IntegrityError as e:
            # Handle any integrity errors, e.g., unique constraints
            messages.error(request, "An error occurred")

            return HttpResponse("An error occurred", status=400)
        except Exception as e:
            # Handle any other exceptions
            return HttpResponse("An unexpected error occurred", status=500)

    # If not POST, render the edit page with the current data
    return render(request, 
        'servicedsi/index.html', 
        {
            'form': form, 
            'page': 'stock',
            'subpage': 'sortie_livraison_tab',
            'sortielivraison_list': sortielivraison_list  # Pass the list to the template
        })
    
@login_required
def delete_sortie_livraison(request, id):
    if request.method == "POST":
        try:
            livraison = get_object_or_404(SortieLivraison, id=id)
            
            reference = livraison.reference
            livraison.is_deleted = True
            livraison.save()
            
            ActionLog.objects.create(
                        product_name=reference,
                        action_done_by=request.user.username,
                        date_deleted=timezone.now(),  # Store the current timestamp as date_deleted
                        type = 'Sortie Livraison',
            
                    )

            # Add a success message
            messages.success(request, "Sortie Livraison deleted successfully.")
        except Exception as e:
            # Log the error or handle it
            messages.error(request, f"An error occurred: {e}")

    return redirect('serviceapresvente:create_sortie_livraison')