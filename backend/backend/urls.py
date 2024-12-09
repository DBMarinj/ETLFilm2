"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # importar rutas dentro de un archivo url de nuestras app
from rest_framework_simplejwt import views as jwtViews# rest framwork ya hizo el login con token

urlpatterns = [
    path('admin/', admin.site.urls),# el framework ya tiene el login creado
    path('token/', jwtViews.TokenObtainPairView.as_view(),# crear token lo asocia al modelo de django
          name ='token_obtain_pair'), # obtener pares de token, crea login
     path('token/refresh/',                                #refrescar token
          jwtViews.TokenRefreshView.as_view(),
          name ='token_refresh'),
    path('', include('authentification.urls')),
    path('', include('AppETL.urls')),             
]
