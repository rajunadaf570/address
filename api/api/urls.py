#django/rest_framework
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

# third part imports.
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

#app level imports
from address import views as address_views

#initialize DefaultRouter
router = SimpleRouter()

#register address app url with router
router.register(r'account', address_views.UserViewSet, base_name='account')
router.register(r'address', address_views.AddressViewSet, base_name='address')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'), namespace='v1')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here

]
