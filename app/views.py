from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics, filters, permissions
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
import django_filters

from accounts.models import Role, User
from accounts.views import IsAdminUser
from .models import UserFacility, Facility, Employee, Revenue
from .models import Importer, ProductionType, Scan, Invoice, Signal, Deduction, WorkHours

from .serializers import WorkHoursSerializer, DeductionsSerializer, SalarySerializer, SignalSerializer, EmployeeSerializer, RevenueSerializer, ImporterSerializer, ProductionTypeSerializer, FacilitySerializer, ScanSerializer, InvoiceSerializer, DashboardRevenueSerializer

from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.http import HttpResponse

import json


class SignalList(generics.ListCreateAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer


class SignalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer


class DeductionsCreate(generics.CreateAPIView):
    serializer_class = DeductionsSerializer


class DeductionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deduction.objects.all()
    serializer_class = DeductionsSerializer


class WorkHoursCreate(generics.CreateAPIView):
    serializer_class = WorkHoursSerializer


class WorkHoursDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkHours.objects.all()
    serializer_class = WorkHoursSerializer


class FacilityList(generics.ListCreateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class FacilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer


class EmployeeFilter(django_filters.FilterSet):

    class Meta:
        model = Employee
        fields = ['facility', ]


class EmployeeList(APIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    ordering_fields = ['full_name', 'phone_number', 'is_active']

    def get(self, request, format=None):
        candidates = Employee.objects.all()
        serializer = EmployeeSerializer(candidates, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile_picture=request.data.get('profile_picture')
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def put(self, request, pk):
        snippet = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object()
        article.delete()
        return Response({
            "message": "Employee with id `{}` has been deleted.".format(pk)
        }, status=204)


class ImporterFilter(django_filters.FilterSet):

    class Meta:
        model = Importer
        fields = ['facility', ]


class ImporterList(generics.ListCreateAPIView):
    #permission_classes = [permissions.IsAuthenticated]

    serializer_class = ImporterSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ImporterFilter
    ordering_fields = ['name', 'production_type', 'comment', ]

    def get_queryset(self):
        facility = self.request.data.get('facility')
        dataset = []
        if not facility and not self.request.user.is_staff:
            # dont return anything
            return Importer.objects.filter()
        elif self.request.user.is_superuser:
            # return all for admins
            return Importer.objects.filter(is_deleted=False)
        else:
            return Importer.objects.filter(is_deleted=False, facility=facility)

    def perform_create(self, serializer):
        serializer.save()


class ImporterDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        #   permissions.IsAuthenticated
    ]
    serializer_class = ImporterSerializer
    queryset = Importer.objects.all()


class ProductionTypeList(generics.ListCreateAPIView):
    queryset = ProductionType.objects.all()
    serializer_class = ProductionTypeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']


class ProductionTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionType.objects.all()
    serializer_class = ProductionTypeSerializer


class RevenueDateFilter(django_filters.FilterSet):
    added_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Revenue
        fields = ['added_at']


class RevenueList(generics.ListCreateAPIView):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['cash_income', 'cash_free_income', 'np', 'added_at']
    filterset_class = RevenueDateFilter


class RevenueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer


class ScanDateFilter(django_filters.FilterSet):
    added_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Scan
        fields = ['added_at']


class ScanClass(generics.ListCreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', 'type_scan', 'file', 'added_at', 'facility']
    filterset_class = ScanDateFilter

    def get(self, request):
        scan = Scan.objects.all()
        serializer = ScanSerializer(scan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ScanSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            saved = serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ScanDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def put(self, request, pk):
        object = Scan.objects.get(pk=pk)
        serializer = ScanSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        importer = self.get_object(pk)
        importer.delete()
        return Response({
            "message": "Employee with id `{}` has been deleted.".format(pk)
        }, status=204)


class InvoiceDateFilter(django_filters.FilterSet):
    added_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Invoice
        fields = ['date']


class InvoiceList(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['date', 'added_by', 'added_at' 'invoice_number', 'amount',
                       'tax_amount', 'importer', 'facility', 'comment', 'payment_type', 'is_confirmed ']
    filterset_class = InvoiceDateFilter

    def get(self, requests):
        invoice = Invoice.objects.all()
        serializer = InvoiceSerializer(invoice, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            invoice_saved = serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class InvoicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class FacilitiForScanApi(APIView):
    queryset = Facility.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    serializer_class = FacilitySerializer

    def get(self, requests):
        facility = Facility.objects.all()
        serializer = FacilitySerializer(facility, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FacilityUserList(generics.ListAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    def get_queryset(self):

        user = self.request.user
        user_facilities = UserFacility.objects.filter(user=user.id)
        facilities = []
        for uf in user_facilities:
            facilities.append(Facility.objects.get(pk=uf.facility))

        return facilities


def get_user_facilities(request):
    user = request.GET["id"]
    q = get_object_or_404(UserFacility, user=user)
    return HttpResponse(json.dumps({"data": q}), content_type="application/json")


class SalaryList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = SalarySerializer
