from rest_framework import serializers
from .models import CabinetLockerRentals, Cabinet, Customer
class CusSer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = ('id', 'name',)

class RentalsSer(serializers.ModelSerializer):
    cus=CusSer(many=True, read_only=True)
    class Meta:
        model=CabinetLockerRentals
        fields=('id','cus','rentdate','fee',)
class usedCabinetCount(serializers.ModelSerializer):
    class Meta:
        model=Cabinet
        fields=('aval',)
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'credentials']

class CabinetLockerRentalsSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()

    class Meta:
        model = CabinetLockerRentals
        fields = ['id', 'rentdate', 'fee', 'customer_name']

    def get_customer_name(self, obj):
        return obj.customerid.name