from rest_framework import viewsets
from apps.leasing.models import Clientleasing
from apps.leasing.api.serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ClientleasingViewSet(viewsets.ModelViewSet):
    queryset = Clientleasing.objects.all()
    serializer_class = ClientleasingSerializer
    pagination_class = None  # If you want to enable pagination, customize this
    
    def get_queryset(self):
        # Override the default to add any custom filtering if needed
        return super().get_queryset()


class ConsommableViewSet(viewsets.ModelViewSet):
    queryset = Consommable.objects.all()
    serializer_class = ConsommableSerializer

    # Optionally, you can override methods if you want custom behavior
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    

class DeploiementViewSet(viewsets.ModelViewSet):
    queryset = Deploiement.objects.all()
    serializer_class = DeploiementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        listeimprimante_id = data.get('listeimprimante').id

        try:
            deploiement_imprimante_instance = Listeimprimante.objects.get(pk=listeimprimante_id)
            deploiement_imprimante_instance.flag = 1
            deploiement_imprimante_instance.save()
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Listeimprimante.DoesNotExist:
            return Response({'detail': 'Listeimprimante not found.'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        listeimprimante_id = data.get('listeimprimante').id

        try:
            deploiement_imprimante_instance = Listeimprimante.objects.get(pk=listeimprimante_id)
            deploiement_imprimante_instance.flag = 1
            deploiement_imprimante_instance.save()
            self.perform_update(serializer)
            return Response(serializer.data)
        except Listeimprimante.DoesNotExist:
            return Response({'detail': 'Listeimprimante not found.'}, status=status.HTTP_400_BAD_REQUEST)


class ExploitationViewSet(viewsets.ModelViewSet):
    queryset = Exploitation.objects.all()
    serializer_class = ExploitationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    
class ClientleasingViewSet(viewsets.ModelViewSet):
    queryset = Clientleasing.objects.all()
    serializer_class = ClientleasingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # If you need to filter the queryset based on the user or other criteria, you can override this method
        return Clientleasing.objects.all()
    

class ListeimprimanteViewSet(viewsets.ModelViewSet):
    queryset = Listeimprimante.objects.all()
    serializer_class = ListeimprimanteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Customize queryset if needed, for example, to filter based on user permissions
        return Listeimprimante.objects.all()