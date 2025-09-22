from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Live reload (optional — remove if not used)
    path('__reload__/', include('django_browser_reload.urls')),

    # Public pages (landing, login, etc.)
    path('', include('apps.pages.urls')),
    
    # Accounts (authentication)
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('tolls/',include('apps.tolls.urls',namespace='tolls')),
    
    # Detections (video upload, AI webhook)
    path('detections/', include('apps.detections.urls', namespace='detections')),

    # Reports app
    path('reports/', include('apps.reports.urls', namespace='reports'))

]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
