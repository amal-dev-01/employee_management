from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomForm
from .serializers import CustomFormSerializer
from django.db import transaction


# ---------------- Form List and Create ----------------
class CustomFormListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        forms = CustomForm.objects.prefetch_related('fields').all()
        serializer = CustomFormSerializer(forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomFormSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    custom_form = serializer.save()
                return Response(CustomFormSerializer(custom_form).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"detail": f"Error creating form: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

