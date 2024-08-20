from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.views.generic import TemplateView,ListView, DetailView, \
                    CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import *
from django.http import JsonResponse
from django.db import IntegrityError
from django.views import View
from django.db.models import F


#####   Gestion CLient
#####

    
class CombinedListView(TemplateView):
    model = Clientleasing  # Spécifiez le modèle que vous utilisez
    template_name = 'leasing/combinedList.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leasingClient'] = Clientleasing.objects.all()
        context['leasingImprimante'] = Listeimprimante.objects.all()
        context['leasingIDeploiement'] = Deploiement.objects.all()
        context['leasingConsommable'] = Consommable.objects.all()
        context['leasingExploitation'] = Exploitation.objects.all()
        context['leasingCategorie'] = typeCategorie.objects.all()
        context['leasingProduit'] = typeProduit.objects.all()
        
        return context


class ClientListView(LoginRequiredMixin,ListView):
    model = Clientleasing
    #Client_Form =ClientleasingForm
    template_name="leasing/client/list.html"
    context_object_name= "clients"
    login_url = reverse_lazy('login')
    
class ClientDetaiView(LoginRequiredMixin,DetailView):
    model = Clientleasing
    template_name = "leasing/client/detail.html"
    context_object_name= "client_details"
    login_url = reverse_lazy('account:login')

    #pk_url_kwarg = 'client_id'
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        client_pk = self.get_object().pk
        #clientName= Clientleasing.objects.get(pk = 1)
        deplois = Deploiement.objects.filter(clientleasing=client_pk)
        print("valeur de deploi:", deplois)
        context["deplois"]= deplois
        return context

class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Clientleasing
    #form_class  = ClientleasingForm
    #template_name="leasing/client/create.html"
    template_name="leasing/client/form.html"
    fields = ['date','refcontrat','nom','adresse','contact','email','localite']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        Clientleasing = form.save(commit=False)
        Clientleasing.userLog = self.request.user
        Clientleasing.save()
        print("Data saved successfully")
        messages.success(self.request, "The task was created successfully.")
        return super(ClientCreateView,self).form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)  

    def get_success_url(self):
        return reverse("leasing:leasing-client-list")
      
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Créer"
        context["titre"] = "SoPresCom  add Leasing"
        return context
    
class ClientUpdateView(LoginRequiredMixin,UpdateView):
    model = Clientleasing
    fields = ['nom','refcontrat','contact','adresse','localite','email']
    #template_name="leasing/client/create.html"
    template_name="leasing/client/form_upd.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        update_user = form.save(commit=False)
        update_user.userLog = self.request.user
        print(update_user.userLog)
        update_user.save()
        print("success")
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)
        #return super(ClientCreateView,self).form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return reverse("leasing:leasing-client-list")
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Modifier"
        context["titre"] = "SoPresCom  Modification Leasing"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        return initial
    
class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Clientleasing
    context_object_name= "client"
    template_name = "leasing/client/delete.html"
    success_url = reverse_lazy("leasing:leasing-client-list")
    login_url = reverse_lazy('login')


#####   Gestion Imprimante
#####
class ImprListView(LoginRequiredMixin,ListView):
    model = Listeimprimante
    template_name="leasing/imprimante/list.html"
    context_object_name= "impri"
    login_url = reverse_lazy('login')

    
class ImprDetaiView(LoginRequiredMixin,DetailView):
    model = Listeimprimante
    template_name = "leasing/imprimante/detail.html"
    context_object_name= "details_impri"
    #pk_url_kwarg = 'client_id'
    login_url = reverse_lazy('login')

    
    #def get_context_data(self, **kwargs) :
    #    context = super().get_context_data(**kwargs)
    #    client = self.get_object().pk
    #    #clientName= Clientleasing.objects.get(pk = 1)
    #    deplois = Deploiement.objects.filter(idclientleasing=client)
    #    context['Titre']= "Detail du Client" #.format
    #    context["deplois"]= deplois
    #    return context

class ImprCreateView(LoginRequiredMixin,CreateView):
    model = Listeimprimante
    #template_name="leasing/imprimante/create.html"
    template_name="leasing/imprimante/form.html"
    form_class = ListeimprimanteForm
    #fields = ['SN','reference','designation','description','date_acquisition','garantie','endoflife']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        formInstance.save()
        print("success")
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
     
    def get_success_url(self):
        return reverse("leasing:leasing-impr-list")
      
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Créer"
        context["titre"] = "Ajout Imprimante"
        return context
    
class ImprUpdateView(LoginRequiredMixin,UpdateView):
    model = Listeimprimante
    #fields = ['designation','description','date_acquisition','garantie']
    form_class = ListeimprimanteForm
    template_name="leasing/imprimante/form_upd.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return reverse("leasing:leasing-impr-list")
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Modifier"
        context["titre"]= "Modif Imprimante"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        return initial
    
class ImprDeleteView(LoginRequiredMixin,DeleteView):
    model = Listeimprimante
    context_object_name= "impri"
    template_name = "leasing/imprimante/delete.html"
    success_url = reverse_lazy("leasing:leasing-impr-list")
    login_url = reverse_lazy('login')



#####   Gestion Deploiement
#####
class DeploieListView(LoginRequiredMixin,ListView):
    model = Deploiement
    template_name="leasing/deploiement/list.html"
    context_object_name= "deploiement"
    login_url = reverse_lazy('login')

class DeploieDetaiView(LoginRequiredMixin,DetailView):    
    model = Deploiement
    template_name = "leasing/deploiement/detail.html"
    context_object_name= "deploiement"
    login_url = reverse_lazy('login')


class DeploieCreateView(LoginRequiredMixin,CreateView):
    model = Deploiement
    form_class = DeploiementForm
    template_name="leasing/deploiement/form.html"
    #fields = ['site','adresseip','date_deploiement','clientleasing','listeimprimante']
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        # Récupérer l'objet Listeimprimante associé et définir flag sur True
        listeimprimante_obj = form.cleaned_data.get('listeimprimante')
        listeimprimante_id = listeimprimante_obj.idlisteimprimante
        listeimprimante = get_object_or_404(Listeimprimante, pk=listeimprimante_id)
        #print('listeimprimante:',listeimprimante)
        #listeimprimante.flag = True
        #print('listeimprimante.flag:',listeimprimante.flag)
        listeimprimante.save()
        # Assigner l'identifiant de l'objet Listeimprimante au champ listeimprimante
        #form_instance.listeimprimante = listeimprimante_id
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        #raise(messages)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse("leasing:leasing-deploie-list")
      
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Créer"
        context["titre"] = "Déploiement"
        return context
    
class DeploieUpdateView(LoginRequiredMixin,UpdateView):
    model = Deploiement
    fields = ['site','adresseip','date_deploiement','clientleasing','listeimprimante']
    template_name="leasing/deploiement/form.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")    
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return reverse("leasing:leasing-deploie-list")
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Modifier"
        context["titre"]= "Modification"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        return initial
    
class DeploieDeleteView(LoginRequiredMixin,DeleteView):
    model = Deploiement
    context_object_name= "deploiement"
    template_name = "leasing/deploiement/delete.html"
    success_url = reverse_lazy("leasing:leasing-deploie-list")  
    login_url = reverse_lazy('login')

#####   Gestion Consommable
#####
class ConsoListView(LoginRequiredMixin,ListView):
    model = Consommable
    template_name="leasing/consommable/list.html"
    context_object_name= "consommable"
    login_url = reverse_lazy('login')

class ConsoDetaiView(LoginRequiredMixin,DetailView):    
    model = Consommable
    template_name = "leasing/consommable/detail.html"
    context_object_name= "consommable"
    login_url = reverse_lazy('login')


class ConsoCreateView(LoginRequiredMixin,CreateView):
    model = Consommable
    template_name="leasing/consommable/form.html"
    form_class = ConsommableForm
    #fields = ['type','bordereausortie','reference','designation','description','typeproduit','quantite']
    login_url = reverse_lazy('login')
    
    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
            
    def get_success_url(self):
        return reverse("leasing:leasing-conso-list")
      
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Créer"
        context["titre"] = "Nouveau Consommable"
        return context
    
class Conso_ajoutstock_View(LoginRequiredMixin,UpdateView):
    model = Consommable
    fields = ['bordereausortie','quantite']
    template_name="leasing/consommable/form_upd_add.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        querySet = Consommable.objects.get(reference = formInstance.reference)
        #print("querySet.quantite: ",querySet)
        stock_add = formInstance.quantite
        formInstance.quantite += querySet.quantite
        formInstance.save()
        messages.success(self.request, "{} with reference {} was added successfully.".format(stock_add,formInstance.designation))
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return reverse("leasing:leasing-conso-list")
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Modifier"
        context["titre"]= "Ajout consommable"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        mymodel = self.get_object()
        #mymodel['quantite']
        initial['bordeausortie'] = ''
        initial['quantite'] = 0
        return initial

class ConsoUpdateView(LoginRequiredMixin,UpdateView):
    model = Consommable
    fields = ['categorieproduit','typeproduit','bordereausortie','reference','designation','description','typeproduit','quantite','seuilLimite']
    template_name="leasing/consommable/form_upd.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return reverse("leasing:leasing-conso-list")
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Modifier"
        context["titre"]= "Mise à jour stock physique"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        return initial
    
class ConsoDeleteView(LoginRequiredMixin,DeleteView):
    model = Consommable
    context_object_name= "consommable"
    template_name = "leasing/consommable/delete.html"
    success_url = reverse_lazy("leasing:leasing-conso-list")  
    login_url = reverse_lazy('login')

#####   Gestion Exploitation
#####

class ExploiListView(LoginRequiredMixin,ListView):
    model = Exploitation
    template_name="leasing/exploitation/list.html"
    context_object_name= "exploitation"
    login_url = reverse_lazy('login')

class ExploiDetaiView(LoginRequiredMixin,DetailView):    
    model = Exploitation
    template_name = "leasing/exploitation/detail.html"
    context_object_name= "exploitation"
    login_url = reverse_lazy('login')


class CreateExploitationView(View):
    template_name = 'leasing/exploitation/form.html'

    def get(self, request, *args, **kwargs):
        form = ExploitationForm()
        formset = ConsommableExploitationFormset()
        context = {
            'form': form,
            'formset': formset
             }
        return render(request, self.template_name,context )

    def post(self, request, *args, **kwargs):
        form = ExploitationForm(request.POST)
        formset = ConsommableExploitationFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            exploitation = form.save(commit=False)
            exploitation = form.save()
            for form in formset:
                if form.cleaned_data:
                    consommable = form.cleaned_data['consommable']
                    quantite = form.cleaned_data['quantite']
            
                    consommable_instance = Consommable.objects.get(pk=consommable.pk)
                    if quantite > consommable_instance.quantite:
                        # Si la quantité est supérieure, afficher un message d'erreur
                        messages.error(request, f"Quantité de {consommable_instance.reference} insuffisante.")
                    else:
                        # Si la quantité est suffisante, déduire la quantité de consommable
                        consommable_instance.quantite = F('quantite') - quantite
                        consommable_instance.save()

                        # Créer la relation dans ConsommableExploitation
                        ConsommableExploitation.objects.create(
                            exploitation=exploitation,
                            consommable =consommable,
                            quantite    =quantite
                        )

            messages.success(request, "Exploitation créée avec succès.")
            return redirect("leasing:leasing-exploi-list")
        else:
            form = ExploitationForm()
            formset = ConsommableExploitationFormset()
        return render(request, self.template_name, {'form': form, 'formset': formset})
"""
class ExploiCreateView(LoginRequiredMixin,CreateView):
    model = Exploitation
    template_name="leasing/exploitation/form.html"
    form_class = ExploitationForm
    #fields = ['intervention','deploiement','consommable','quantite','pourcentage_toner','ancien_index','nouvel_index','observation']
    login_url = reverse_lazy('login')

    def fom_valid(self,form):
        context = self.get_context_data()
        consommable_formset = context['consommable_formset']
        if consommable_formset.is_valid():
            self.object = form.save()
            consommable_formset.instance = self.object
            consommable_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
        #formInstance = form.save(commit=False)
        #formInstance.userLog = self.request.user
        #formInstance.save()
        #messages.success(self.request, "The task was created successfully.")
        #return super().form_valid(form)
        

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def post(self,request,  *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            conso = form.cleaned_data['consommable']
            quantite = form.cleaned_data['quantite']
            obj.userLog =  self.request.user
            querySet = Consommable.objects.get(reference = conso[0]) 
            print("Quantité input:", quantite)
            print("Quantité en stock:",querySet.quantite)
            if quantite <= querySet.quantite:
                obj.save()
                form.save_m2m()
                querySet.quantite -= quantite
                querySet.save()
                return redirect('leasing:leasing-exploi-list')
            else: 
                print("affichage erreur...")
                messages.error(self.request,'Stock restant:{} pour la référence demandée'.format(querySet.quantite))
                return redirect('leasing:leasing-exploi-create') 
               
    def get_success_url(self):
        return reverse("leasing:leasing-exploi-list")
      
    #def get_context_data(self, **kwargs) :
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['consommable_formset'] = ConsommableFormSet(self.request.POST)
        else:
            data['consommable_formset'] = ConsommableFormSet()
        data["submit_text"]= "Créer"
        data["Titre"] = "New Client"    
        return data

"""        
    
class ExploiUpdateView(LoginRequiredMixin,UpdateView):
    model = Exploitation
    fields = ['intervention','deploiement','consommable','quantite','pourcentage_toner',
              'ancien_index','nouvel_index','description']
    template_name="leasing/exploitation/form.html"
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        formInstance.userLog = self.request.user
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
    
    def post(self,request,  *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            conso = form.cleaned_data['consommable']
            quantite = form.cleaned_data['quantite']
            obj.userLog =  self.request.user
            querySet = Consommable.objects.get(reference = conso[0]) 
            print("Quantité input:", quantite)
            print("Quantité en stock:",querySet.quantite)
            if quantite <= querySet.quantite:
                obj.save()
                form.save_m2m()
                querySet.quantite -= quantite
                querySet.save()
                return redirect('leasing:leasing-exploi-list')
            else: 
                print("affichage erreur...")
                messages.error(self.request,'Stock restant:{} pour la référence demandée'.format(querySet.quantite))
                #messages.add_message(self.request, messages.error,'Unable to add thos quantity')
               
                #raise PermissionDenied("Il ne reste en stock que: {} pour la reference:{}".format(querySet.quantite,querySet.designation))        
                return redirect('leasing:leasing-exploi-create') 
            
    def get_success_url(self) -> str:
        return reverse("leasing:leasing-exploi-list")
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Modifier"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        return initial
    
class ExploiDeleteView(LoginRequiredMixin,DeleteView):
    model = Exploitation
    context_object_name= "exploitation"
    template_name = "leasing/exploitation/delete.html"
    success_url = reverse_lazy("leasing:leasing-exploi-list")  
    login_url = reverse_lazy('login')


def ReportLeasing(request):
    AllImp = ''
    refAgg = ''
    ImprimanteDeploye = 0
    ImprimanteNonDeploye = 0
    RefImpStatut = ''
    clientleasing = Clientleasing.objects.all()
    AllImp,refAgg,ImpStatus,RefImpStatut = Listeimprimante.LeasingStatImprimante()
    conso = Consommable.select_conso_stock()
    #print('AllImp:',AllImp)
    #print('refAgg:',refAgg)
    #print('ImpStatus:',ImpStatus)
    #print('RefImpStatut:',RefImpStatut)
    consomTab=[]
    print('conso:',conso)
    for row in conso:
        pass
    
    lientLeasingTab = []
    #print('clientleasing:',clientleasing)
    for row in clientleasing:
        detail = {
            'name':row['nom']
        }
        lientLeasingTab.append(detail)
    refAggTab = []
    for row in refAgg:
        detail = {
            'reference':row['reference'],
            'nombre':row['status_count']
        }
        refAggTab.append(detail)
    for row in ImpStatus:
        if row['flag'] == False:
            ImprimanteNonDeploye =  row['status_count'] 
        if row['flag'] == True: 
            ImprimanteDeploye =  row['status_count'] 
            #print('ImprimanteDeploye:',ImprimanteDeploye)
    RefImpStatutTab = []
    for row in RefImpStatut:
        if row['flag'] == False:
                status= 'Non déployée'
        else: 
            status = 'deployée'        
        detail = {
            'reference':row['reference'],
            'flag': status,
            'nombre':row['status_count']
        }
        RefImpStatutTab.append(detail)  
    #print('lientLeasingTab:',lientLeasingTab)      
    Jsonresult={
            'lientLeasingTab':lientLeasingTab,
            'NbreImpr':AllImp,
            'refAggTab':refAggTab,
            'ImprimanteDeploye':ImprimanteDeploye,
            'ImprimanteNonDeploye':ImprimanteNonDeploye,
            'RefImpStatutTab':RefImpStatutTab,
        }
    return JsonResponse(Jsonresult,safe=False)
    
def get_typeProduit_by_categorie(request):
    categorieID = request.GET.get('categorie')
    typeproduit = typeProduit.get_typeProduit_byCategorieID(categorieID)
    details = []
    #for row in typeproduit:
    #    detail = {
    #        'id':row['idtypeproduit'],
    #        'designation':row['designation'],
    #    }
    #    details.append(detail) 
    #print('JSON retour:',list(typeproduit))
    #return JsonResponse(details, safe=False)
    return JsonResponse(list(typeproduit), safe=False)



class CategoryListView(LoginRequiredMixin,ListView):
    model = typeCategorie
    template_name="leasing/categorie/listCategorie.html"
    context_object_name= "categorie"
    login_url = reverse_lazy('login')

class ProduitListView(LoginRequiredMixin,ListView):
    model = typeProduit
    template_name="leasing/categorie/listProduit.html"
    context_object_name= "categorie"
    login_url = reverse_lazy('login')

    
"""
class CategoryCreateView(LoginRequiredMixin,CreateView):
    model = Consommable
    template_name="leasing/categorie/form.html"
    form_class = ConsommableForm
    #fields = ['type','bordereausortie','reference','designation','description','typeproduit','quantite']
    login_url = reverse_lazy('login')
    
    def form_valid(self, form):
        #form.instance.user = self.request.user
        formInstance = form.save(commit=False)
        #formInstance.userLog = self.request.user
        formInstance.save()
        messages.success(self.request, "The task was created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Print the errors to the console
        for field in form.errors:
            for error in form.errors[field]:
                print(f"{field}: {error}")
                messages.error(self.request, f"{field}: {error}")
        # Call the parent form_invalid method to display errors in the template
        return super().form_invalid(form)
            
    def get_success_url(self):
        return reverse("leasing:leasing-conso-list")
      
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["submit_text"]= "Créer"
        context["titre"] = "Nouvelle catégorie"
        return context
"""
@receiver(post_save, sender=Consommable)
def update_HistioriqueConsommable(sender, instance, created, **kwargs):
    obj = HistioriqueConsommable(
          date = instance.date,
          bordereausortie = instance.bordereausortie,
          reference = instance.reference,
          designation = instance.designation,
          description = instance.description,
          typeproduit = instance.typeproduit,
          quantite = instance.quantite,
          userLog = instance.userLog
        )
    obj.save()

    
