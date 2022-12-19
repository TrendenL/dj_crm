from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from leads.views import landing_page, LandingPageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_views(), name="login" ),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("leads/", include("leads.urls", namespace="leads")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
