from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from .serializer import *
from rest_framework.decorators import api_view 
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import APIView

# Create your views here.



@api_view(['GET','POST'])
def user(request):
    if request.method == "GET":
        try:
            object = CustomUser.objects.all()
            serializer = CustomUerSerializer(object,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    elif request.method == "POST":
        try:
            validated = request.data
            cus = {
                'email': validated.get('email'),
                'display_name' : validated.get('display_name'),
            }
            custom_serializer = CustomUerSerializer(data=validated)
            
            if custom_serializer.is_valid():
                custom_obj = CustomUser.objects.create(**cus)
                custom_obj.set_password(validated.get('password'))
                custom_obj.save()
                return Response("User register successfully", status=status.HTTP_201_CREATED)
            else:
                return Response(custom_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 

#-----------------------------------------------------------LOGIN--------------------------------------------------



class LoginView(APIView):
    def post(self,request):
        try:
            data = request.data 
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                try:
                    email = serializer.data['email']
                    password = serializer.data['password']
                    user = authenticate(email=email,password=password)
                    if user is None:
                        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    return Response({
                        'refresh': str(refresh),
                        'access': str(access_token),
                       
                    }) 
                except Exception as e:
                    return Response({"error": f"Error during authentication: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)      
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    




 
#---------------------------------------------------------LOGOUT---------------------------------------------------



class logoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('\n',request.data,'\n')
        
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"Message":"Enter refresh_token"})
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Success"},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        








class taskview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
 

    def get(self,request):
        try:
            request.data
            obj = Task.objects.all()
            serializer_obj = TaskSerializer(obj,many=True)
            return Response(serializer_obj.data)
    
        except Exception as e:
            return Response({"error":f"Unexpected error:{str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def post(self,request):
        try:
            validated_data = request.data
            serializer_obj = TaskSerializer(data=validated_data)

            if serializer_obj.is_valid():
                serializer_obj.save()
                return Response({'Message':'Task Created Successfully ',"Data":serializer_obj.data},status=status.HTTP_201_CREATED)
            
            else:
                return Response({"Message":serializer_obj.errors},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error":f"Unexcepted error :{str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self,request,id):

        try:
                obj = Task.objects.get(id = id)
            
        except Task.DoesNotExist:
                return Response({"Message":"Address not found "},status=status.HTTP_404_NOT_FOUND)
            
        serializers_obj = TaskSerializer(obj, data=request.data, partial=True)
            
        if serializers_obj.is_valid():
                serializers_obj.save()
                return Response({"Message":"Task Updated Successfully ","Data":serializers_obj.data},status=status.HTTP_201_CREATED)
            
        else:
            return Response({"Message":serializers_obj.errors},status=status.HTTP_400_BAD_REQUEST)
            
        



    def delete(self,request,id):
        try:
                request.data
                try:
                    pro_obj = Task.objects.get(id = id)
                    pro_obj.delete()
                    return Response({"Message":"Data Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
                
                except Task.DoesNotExist:
                    return Response({"Message":" task Not Found"},status=status.HTTP_404_NOT_FOUND)
                
            
        except Exception as e:
            return Response({"Error":f"Unexcepted error {str(e)}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

