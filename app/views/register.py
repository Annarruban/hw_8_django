from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from app.serializers import RegisterSerializer
from app.utils import set_jwt_cookies


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
        )
        
        user = serializer.save()
        response = Response({
            'user': {
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)
        set_jwt_cookies(response, user)
        return response
