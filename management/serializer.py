from rest_framework import serializers
from .models import EmployeeForm,EmployeeManagement

class EmployeeFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeForm
        fields = '__all__'
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            print(attr, value, validated_data)
            setattr(instance, attr, value)

        instance.save()
        return instance


class EmployeeManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeManagement
        fields = ['form', 'dynamic_data']