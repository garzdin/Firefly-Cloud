from json import dumps
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from models import User

from rest_framework import routers, serializers, viewsets

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'first_name' in request.POST and 'last_name' in request.POST and 'email' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                pass
            else:
                return HttpResponse(dumps({"message": "A user with that username already exists."}), content_type='application/json')
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                pass
            else:
                return HttpResponse(dumps({"message": "A user with that email already exists."}), content_type='application/json')
            if password < 6:
                return HttpResponse(dumps({"message": "Password should be at least 6 characters."}), content_type='application/json')
            try:
                validate_email(email)
            except ValidationError:
                return HttpResponse(dumps({"message": "Email is invalid."}), content_type='application/json')
            user = User.objects.create_user(username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            return HttpResponse(dumps({"message": "User was created successfully."}), content_type='application/json')
        else:
            return HttpResponse(dumps({"message": "Not enough parameters provided."}), content_type='application/json')
    else:
        return HttpResponse(dumps({"message": "Invalid request."}), content_type='application/json')

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return HttpResponse(dumps({"message": "A user with that username doesn't exist."}), content_type='application/json')
            else:
                if user.check_password(password):
                    return HttpResponse(dumps({"api_key": user.api_key}), content_type='application/json')
                else:
                    return HttpResponse(dumps({"message": "Invalid password."}), content_type='application/json')
        else:
            return HttpResponse(dumps({"message": "Not enough parameters provided."}), content_type='application/json')
    else:
        return HttpResponse(dumps({"message": "Invalid request."}), content_type='application/json')

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
