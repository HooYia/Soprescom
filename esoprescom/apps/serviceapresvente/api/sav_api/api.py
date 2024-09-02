
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.serviceapresvente.models import Sav_request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .serializers import SavRequestSerializer

class SavRequestPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

class SavRequestListView(APIView):
    def get(self, request):
        # Check user permissions
        if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_losgistic):
            return Response({"detail": "Not authorized"}, status=403)

        sav_requests = Sav_request.objects.all()
        paginator = SavRequestPagination()
        paginated_requests = paginator.paginate_queryset(sav_requests, request)

        serializer = SavRequestSerializer(paginated_requests, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
    
class SavRequestCreateView(APIView):
    def post(self, request):
        if not (request.user.is_superuser or request.user.is_staff or request.user.is_compta or request.user.is_recouvrement or request.user.is_logistic):
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = SavRequestSerializer(data=request.data)
        if serializer.is_valid():
            sav_request = serializer.save(userLog=request.user)
            if sav_request.bon_pour_accord:
                # Additional logic for bon_pour_accord
                messages.info(request, 'Processus Achat !')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavRequestDetailView(APIView):
    def get(self, request, id):
        sav_request = get_object_or_404(Sav_request, idrequest=id)
        serializer = SavRequestSerializer(sav_request)
        return Response(serializer.data)

class SavRequestUpdateView(APIView):
    def put(self, request, id):
        sav_request = get_object_or_404(Sav_request, idrequest=id)
        serializer = SavRequestSerializer(sav_request, data=request.data)

        if serializer.is_valid():
            serializer.save(userLog=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavRequestDeleteView(APIView):
    def delete(self, request, id):
        sav_request = get_object_or_404(Sav_request, idrequest=id)
        sav_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)