from django.contrib import admin
from django.urls import path
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Emids",
        default_version='v1',
        description="Welcome to the world of Emids Project",
        terms_of_service="#",
        contact=openapi.Contact(email="mvp@emids.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    path('', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/pharmacy/', include('pharmacy.urls')),
]
