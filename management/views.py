from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import EmployeeForm,EmployeeManagement
from .serializer import EmployeeFormSerializer

class EmployeeFormView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            employee_profile = EmployeeForm.objects.filter(created_by=request.user)
        except EmployeeManagement.DoesNotExist:
            return Response({"message": "Employee profile not found!"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"dynamic_data": employee_profile.values()}, status=status.HTTP_200_OK)
        

    def put(self, request):
        data = {"dynamic_fields": request.data}
        try:
            print(data, request.user)
            employee_form, _ = EmployeeForm.objects.get_or_create(created_by=request.user)
            print(employee_form, _)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = EmployeeFormSerializer(instance=employee_form, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class UpdateEmployeeFormDataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, profile_id=None):
        try:

            search_params = request.query_params
            search_key, search_value = None, None

            if search_params:
                search_key, search_value = list(search_params.items())[0]

            query = EmployeeManagement.objects.filter(form__created_by=request.user)

    
            if search_key and search_value.strip():
                query = query.filter(**{f"dynamic_data__{search_key}__icontains": search_value.strip()})

            if profile_id:
                query = query.filter(id=profile_id)

            employee_data = query.values()

            return Response(
                {"dynamic_data": employee_data},
                status=status.HTTP_200_OK,
            )

        except EmployeeManagement.DoesNotExist:
            return Response(
                {"message": "Employee profile not found!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
    def post(self, request):
        new_data = request.data
        employee_profile = EmployeeForm.objects.filter(created_by=request.user)
        EmployeeManagement.objects.create(
            dynamic_data=new_data,
            form=employee_profile[0])
        return Response({"message": "Form data created successfully!"}, status=status.HTTP_200_OK)
    
    def patch(self, request, profile_id):
        try:
            employee_profile = EmployeeManagement.objects.get(id=profile_id)
        except EmployeeManagement.DoesNotExist:
            return Response({"message": "Employee profile not found!"}, status=status.HTTP_404_NOT_FOUND)
        new_data = request.data
        print(new_data,'.......')
        employee_profile.dynamic_data.update(new_data)
        employee_profile.save()
        print(employee_profile)
        return Response({"message": "Form data updated successfully!"}, status=status.HTTP_200_OK)

    def delete(self, request, profile_id):
        try:
            employee_profile = EmployeeManagement.objects.get(id=profile_id)
        except EmployeeManagement.DoesNotExist:
            return Response({"message": "Employee profile not found!"}, status=status.HTTP_404_NOT_FOUND)
        employee_profile.delete()
        return Response({"message": "Employee profile deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

        