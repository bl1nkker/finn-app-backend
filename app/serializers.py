from rest_framework import serializers
from .models import Facility, Importer, ProductionType, WorkHours, Deduction
from .models import UserFacility, Employee, Revenue, Invoice, Scan, Signal


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class UserFacilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFacility
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Employee
        fields = '__all__'


class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = '__all__'


class ProductionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionType
        fields = '__all__'


class ImporterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Importer
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'


class DashboardRevenueSerializer(serializers.Serializer):
    revenue = serializers.IntegerField()


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = '__all__'


class WorkHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHours
        fields = '__all__'


class DeductionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    work_hours = WorkHoursSerializer(many=True)
    deductions = DeductionsSerializer(many=True)

    class Meta:
        model = Employee
        fields = '__all__'
