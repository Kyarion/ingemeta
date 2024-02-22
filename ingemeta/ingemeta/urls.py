"""
URL configuration for ingemeta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from gestion import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name = 'home'),
    path('registro/', views.registro_usuario, name='registro'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name = 'logout'),
    path('crear-orden-compra/', views.crear_orden_compra, name='crear_orden_compra'),
    path('orden-compra/<int:pk>/', views.detalle_orden_compra, name='detalle_orden_compra'),
    path('orden-compra/<int:pk>/modificar-prioridad/', views.modificar_prioridad, name='modificar_prioridad'),
    path('orden-compra/', views.lista_ordenes_compra, name='lista_ordenes_compra'),
    path('produccion/', views.produccion, name='produccion'),
    path('produccion/cambio_rollo/', views.cambio_rollo, name='cambio_rollo'),
    path('produccion/fin_produccion/', views.fin_produccion, name='fin_produccion'),
    path('despacho/', views.despacho, name='despacho'),
    path('ingreso-material/', views.ingreso_material, name='ingreso_material'),
    path('setup-ajustes/', views.setup_ajustes, name='setup_ajustes'),
    path('pana-mantencion/', views.pana_mantencion, name='pana_mantencion'),
    path('produccion-iniciar/', views.produccion_iniciar, name='produccion_iniciar'),
]
