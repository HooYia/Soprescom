
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.accounts.views import homeviewapi
from config.auth_urls import urlpatterns as registration_urls


schema_view = get_schema_view(
    openapi.Info(
        title="Soprescom",
        default_version='v1',
        description='Soprescom',
        terms_of_service='',
        contact=openapi.Contact(email='contact@sopres.com'),
        license=openapi.License(name='BSD license')

    ),

    public=True,
    permission_classes=[permissions.IsAdminUser],
)

swagger_urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_kwargs=0), name='schema-redoc')
]

v1='api/v1/'

auth_api_patterns = [
    path('auth/', include(registration_urls)),
]


urlpatterns = [
    path('', include('apps.shop.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('sav/', include('apps.serviceapresvente.urls')),
    path('leasing/', include('apps.leasing.urls')),
   
    path('admin/', admin.site.urls),
     

    
    #api's
    # path(f'{v1}', include(auth_api_patterns)),
    path('api/v1/', homeviewapi, name='index'),
    path(f'{v1}', include(swagger_urlpatterns)),
    path(f'{v1}', include(auth_api_patterns)),
    path(f'{v1}', include('config.router')),

    
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )