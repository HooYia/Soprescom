from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.serviceapresvente.models import Instance, Instance_recouvrement
from apps.serviceapresvente.api.instance.serializers import *

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer

    def perform_create(self, serializer):
        serializer.save(userLog=self.request.user)
        instance = serializer.instance
        if instance.is_facturable:
            instance_recouv, created = Instance_recouvrement.objects.get_or_create(
                instance_id=instance.idinstance
            )
            if created:
                instance.flag = True
                instance.statut = 'Non Payé'
                instance.save()

    def perform_update(self, serializer):
        serializer.save(userLog=self.request.user)
        instance = serializer.instance
        if instance.is_facturable and instance.statut == 'Résolu':
            instance_recouv, created = Instance_recouvrement.objects.get_or_create(
                instance_id=instance.idinstance
            )
            if created:
                instance.flag = True
                instance.statut = 'Non Payé'
                instance.save()

class InstanceRecouvrementViewSet(viewsets.ModelViewSet):
    queryset = Instance_recouvrement.objects.all()
    serializer_class = InstanceRecouvrementSerializer

    def perform_update(self, serializer):
        serializer.save(userLog=self.request.user)
        instance_recouv = serializer.instance
        if instance_recouv.facture_statut == 'Payé':
            instance_recouv.flag = True
            instance_recouv.save()
