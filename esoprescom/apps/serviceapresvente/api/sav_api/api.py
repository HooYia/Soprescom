from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.serviceapresvente.models import Sav_request, Client_sav, CommandeSav, SuiviCommandeSav
from apps.accounts.models import Customer
from django.db.utils import IntegrityError
from .serializers import *
from rest_framework.permissions import IsAuthenticated



class SavRequestViewSet(viewsets.ModelViewSet):
    queryset = Sav_request.objects.all()
    serializer_class = SavRequestSerializer

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        sav_request = get_object_or_404(Sav_request, pk=pk)
        serializer = self.get_serializer(sav_request)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        sav_request = get_object_or_404(Sav_request, pk=pk)
        serializer = self.get_serializer(sav_request, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        sav_request = get_object_or_404(Sav_request, pk=pk)
        sav_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='create-client')
    def create_client(self, request):
        try:
            user_log_id = request.data.get('userLog')
            nom = request.data.get('nom')
            prenom = request.data.get('prenom')
            telephone = request.data.get('telephone')
            adresse = request.data.get('adresse')
            customer = get_object_or_404(Customer, id=user_log_id)

            if Client_sav.objects.filter(customer=customer).exists():
                return Response({'success': False, 'message': 'A client with the same details already exists!'})

            data = {
                'client_name': f"{nom} {prenom}",
                'telephone': telephone,
                'adresse': adresse,
                'customer': customer,
                'nom': nom,
                'prenom': prenom,
                'userLog': request.user.email,
            }

            client = Client_sav.objects.create(**data)

            # send the email as done in your view
            # send_email_with_template_customer.delay(subject, template_name, context, to_email, from_email)

            return Response({
                'success': True,
                'message': 'Client added successfully!',
                'client_id': client.idclient,
                'client_name': client.client_name
            })

        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CommandeSavViewSet(viewsets.ModelViewSet):
    queryset = CommandeSav.objects.all()
    serializer_class = CommandeSavSerializer

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        commandesav = get_object_or_404(CommandeSav, pk=pk)
        serializer = self.get_serializer(commandesav)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        
        if data.statut == "commande placée":
            try:
                suicommandesav, created = SuiviCommandeSav.objects.get_or_create(
                    commandesav_id=data.idcommandesav,
                )
                if created:
                    sav_request_instance = Sav_request.objects.get(pk=data.savrequest.idrequest)
                    sav_request_instance.statut = 'pending (logistique)'
                    sav_request_instance.save()
                    data.flag = True
                    data.save()
                    return Response({'success': True, 'message': 'Processus Logistique!'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'warning': 'Le suivi de commande existe déjà.'}, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({'error': 'Erreur d\'intégrité lors de la création du processus achat !'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': True, 'message': 'CommandeSav has been saved!'}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        commandesav = get_object_or_404(CommandeSav, pk=pk)
        serializer = self.get_serializer(commandesav, data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        if data.statut == "commande placée":
            try:
                suicommandesav, created = SuiviCommandeSav.objects.get_or_create(
                    commandesav_id=data.idcommandesav,
                )
                if created:
                    sav_request_instance = Sav_request.objects.get(pk=data.savrequest.idrequest)
                    sav_request_instance.statut = 'pending (logistique)'
                    sav_request_instance.save()
                    data.flag = True
                    data.save()
                    return Response({'success': True, 'message': 'Processus Logistique!'}, status=status.HTTP_200_OK)
                else:
                    return Response({'warning': 'Le suivi de commande existe déjà.'}, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response({'error': 'Erreur d\'intégrité lors de la création du processus achat !'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': True, 'message': 'CommandeSav has been updated!'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        commandesav = get_object_or_404(CommandeSav, pk=pk)
        commandesav.delete()
        return Response({'success': True, 'message': 'CommandeSav has been deleted!'}, status=status.HTTP_204_NO_CONTENT)


class SuiviCommandeSavViewSet(viewsets.ModelViewSet):
    queryset = SuiviCommandeSav.objects.all()
    serializer_class = SuiviCommandeSavSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.statut == SuiviCommandeSav.ETAT.LIVRER:
            assemblage, created = AssemblageReparation.objects.get_or_create(
                suivicommandesav_id=instance.idsuivicommandesav,
            )
            if created:
                Sav_request_instance = instance.commandesav.savrequest
                Sav_request_instance.statut = 'pending (DSI - Assemblage)'
                Sav_request_instance.save()
                
                
class LivraisonClientViewSet(viewsets.ModelViewSet):
    queryset = LivraisonClient.objects.all()
    serializer_class = LivraisonClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        Sav_request_instance = instance.assamblagereparation.suivicommandesav.commandesav.savrequest
        if instance.statut == LivraisonClient.Livraison.LIVRE:
            recouvrement, created = Recouvrement.objects.get_or_create(
                livraisonclient_id=instance.idlivraisonclient,
                is_devea_request=Sav_request_instance.recouvrement_hp
            )
            if created:
                if Sav_request_instance.recouvrement_hp:
                    Sav_request_instance.statut = 'Dossier HP à completer'
                else:
                    Sav_request_instance.statut = 'Sav non payé'
                Sav_request_instance.save()
                instance.flag = True
                instance.save()
                

class AssemblageReparationViewSet(viewsets.ModelViewSet):
    queryset = AssemblageReparation.objects.all()
    serializer_class = AssemblageReparationSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.statut == AssemblageReparation.ETAT.TERMINER:
            try:
                livraison, created = LivraisonClient.objects.get_or_create(
                    assamblagereparation_id=instance.idassemblage,
                )
                if created:
                    Sav_request_instance = Sav_request.objects.get(pk=instance.suivicommandesav.commandesav.savrequest.idrequest)
                    Sav_request_instance.statut = 'SAV non Livré(e)'
                    Sav_request_instance.save()
                    instance.flag = True
                    instance.save()
                    # Logging the success of the process (you can replace this with an actual logger)
                else:
                    # If the LivraisonClient entry was not newly created, log this
                    # Optionally, you can also return a response indicating no new creation
                    return Response({"detail": "No new LivraisonClient entry created, already exists."}, status=status.HTTP_200_OK)
            except IntegrityError:
                # Log the integrity error and return an appropriate response
                return Response({"error": "Integrity error during process creation."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If the status is not 'Terminé', proceed as usual
            instance.save()
            return Response({"detail": "AssemblageReparation updated successfully."}, status=status.HTTP_200_OK)
        
        
class ClotureDossierViewSet(viewsets.ModelViewSet):
    queryset = ClotureDossier.objects.all()
    serializer_class = ClotureDossierSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned results to a given user.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or user.is_staff or user.is_compta or user.is_recouvrement or user.is_logistic):
            queryset = queryset.none()  # Return an empty queryset if the user is not authorized
        return queryset
    
    
class PersonnelsViewSet(viewsets.ModelViewSet):
    queryset = Personnels.objects.all()
    serializer_class = PersonnelsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or user.is_staff or user.is_compta or user.is_recouvrement or user.is_logistic):
            queryset = queryset.none()
        return queryset
    
    
class PartenairesViewSet(viewsets.ModelViewSet):
    queryset = Partenaires.objects.all()
    serializer_class = PartenairesSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned results based on user permissions.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or user.is_staff or user.is_compta or user.is_recouvrement or user.is_logistic):
            queryset = queryset.none()  # Return an empty queryset if the user is not authorized
        return queryset
    

class RecouvrementViewSet(viewsets.ModelViewSet):
    queryset = Recouvrement.objects.all()
    serializer_class = RecouvrementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restrict the returned results based on user permissions.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or user.is_staff or user.is_compta or user.is_recouvrement or user.is_logistic):
            queryset = queryset.none()  # Return an empty queryset if the user is not authorized
        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_devea_request:
            if instance.statutDevea == "Dossier HP payé":
                self._process_compta(instance)
        elif instance.statut == "Sav payé":
            self._process_compta(instance)

    def _process_compta(self, recouvrement):
        try:
            cloturedossier, created = ClotureDossier.objects.get_or_create(
                recouvrement_id=recouvrement.idrecouvrement
            )
            if created:
                sav_request_instance = Sav_request.objects.get(
                    pk=recouvrement.livraisonclient.assamblagereparation.suivicommandesav.commandesav.savrequest.idrequest
                )
                sav_request_instance.statut = 'Dossier clôturé et payé'
                sav_request_instance.save()
                recouvrement.flag = True
                recouvrement.save()

                cloturedossier.numero_dossier = sav_request_instance.numero_dossier
                cloturedossier.client = sav_request_instance.client_sav.name
                cloturedossier.resp_dossier = sav_request_instance.resp_sav.name
                cloturedossier.statut = sav_request_instance.statut
                cloturedossier.save()
        except IntegrityError:
            # Log or handle the integrity error
            pass
        

class Sav_InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally restrict the returned results based on user permissions.
        """
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or user.is_staff or user.is_compta or user.is_recouvrement or user.is_logistic):
            queryset = queryset.none()  # Return an empty queryset if the user is not authorized
        return queryset

    def perform_update(self, serializer):
        instance = serializer.save()
        # Add custom logic here if needed, e.g., handling flags or other fields
        # Example: Check and update flags
        if instance.flag and not instance.flag2:
            # Do something specific if flag is True and flag2 is False
            pass